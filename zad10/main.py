from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split, lower, regexp_replace, length, input_file_name, expr
from pyspark.ml.feature import StopWordsRemover, HashingTF, IDF
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Initialize Spark session
spark = SparkSession.builder.appName("WordCloud").getOrCreate()

# Read all text files under the "shakespear/" directory
text_df = spark.read.text("shakespear/*.txt", wholetext=True).withColumn("filename", input_file_name())

# Remove punctuation and convert to lowercase
text_df = text_df.withColumn("text", lower(regexp_replace(col("value"), "[^a-zA-Z\\s]", "")))

# Split text into words
words_df = text_df.withColumn("words", split(col("text"), "\\s+"))

# Remove empty words, words that are whitespace only, and words shorter than 3 characters
words_df = words_df.withColumn("words", expr("filter(words, x -> length(trim(x)) > 2)"))

# Remove stop words
remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
filtered_df = remover.transform(words_df)

# Select only the filtered words column and filename
filtered_df = filtered_df.select("filtered_words", "filename")

# Compute term frequency (TF)
hashingTF = HashingTF(inputCol="filtered_words", outputCol="raw_features")
featurized_df = hashingTF.transform(filtered_df)

# Compute inverse document frequency (IDF)
idf = IDF(inputCol="raw_features", outputCol="features")
idf_model = idf.fit(featurized_df)
tfidf_df = idf_model.transform(featurized_df)

# Collect the TF-IDF features and words
tfidf_features = tfidf_df.select("filtered_words", "features", "filename").collect()

# Generate word clouds for each document
for row in tfidf_features:
    words = row["filtered_words"]
    features = row["features"].toArray()
    filename = row["filename"]
    
    # Create a dictionary of words and their TF-IDF scores
    word_tfidf = {words[i]: features[i] for i in range(len(words))}
    
    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_tfidf)
    
    # Display the word cloud with filename as title
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    trimmed_filename = filename.split("/")[-1]
    plt.title(trimmed_filename, fontsize=12)
    plt.axis("off")
    plt.show()

# Stop Spark session
spark.stop()