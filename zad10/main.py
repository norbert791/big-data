from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower, length, col, desc
from pyspark.ml.feature import Tokenizer, StopWordsRemover
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def process_shakespeare_text(file_path):
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("ShakespeareTextAnalysis") \
        .getOrCreate()

    # Read text file
    text_df = spark.read.text(file_path)

    # Tokenize text
    tokenizer = Tokenizer(inputCol="value", outputCol="words")
    words_df = tokenizer.transform(text_df)

    # Preprocess words
    processed_words = words_df.select(
        explode("words").alias("word")
    ).filter(
        (length(col("word")) > 2) & 
        (col("word") != "")
    )

    filtered_df = processed_words.select("word")

    # Remove stop words
    remover = StopWordsRemover(inputCol="word", outputCol="filtered_words")
    remover.setCaseSensitive(False)
    remover.setStopWords(remover.loadDefaultStopWords("english"))
    print(processed_words.head())
    filtered_df = remover.transform(processed_words)

    
    # Count word frequencies
    word_counts = filtered_df \
        .groupBy("word") \
        .count() \
        .orderBy(desc("count"))

    # Generate word cloud
    word_freq_dict = {row['word']: row['count'] for row in word_counts.collect()}
    
    wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(word_freq_dict)
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig('shakespeare_wordcloud.png')
    plt.close()

    # Show top 20 words
    print("Top 20 words:")
    word_counts.show(20)

    # Close Spark session
    spark.stop()

    return word_counts

# Example usage
results = process_shakespeare_text("./shakespear/hamlet.txt")