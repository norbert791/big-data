from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split, lower, regexp_replace, length
from pyspark.ml.feature import StopWordsRemover
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Initialize Spark session
spark = SparkSession.builder.appName("WordCloud").getOrCreate()

# Read text file
text_df = spark.read.text("shakespear/hamlet.txt")

# Preprocess text: convert to lowercase, remove punctuation, and split into words
words_df = text_df.select(split(lower(regexp_replace(col("value"), "[^a-zA-Z\\s]", "")), "\\s+").alias("words"))

# Remove stop words and words of length shorter than 3
remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
remover.loadDefaultStopWords("english")
filtered_df = remover.transform(words_df)

# Explode the filtered words into individual rows
filtered_words_df = filtered_df.select(explode(col("filtered_words")).alias("word"))
filtered_words_df = filtered_words_df.filter(length(col("word")) >= 3)

# Count occurrences of each word
word_counts = filtered_words_df.groupBy("word").count().orderBy("count", ascending=False)

# Get the 20 most popular words
top_words = word_counts.limit(20).collect()

# Convert to dictionary for word cloud
word_freq = {row['word']: row['count'] for row in top_words}

# Generate word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# Stop Spark session
spark.stop()