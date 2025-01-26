from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split, lower, regexp_replace, length, input_file_name
from pyspark.ml.feature import StopWordsRemover, HashingTF, IDF
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Initialize Spark session
spark = SparkSession.builder.appName("WordCloud").getOrCreate()

# Read all text files under the "shakespear/" directory
text_df = spark.read.text("shakespear/*.txt").withColumn("filename", input_file_name())

# Preprocess text: convert to lowercase, remove punctuation, and split into words
words_df = text_df.select(split(lower(regexp_replace(col("value"), "[^a-zA-Z\\s]", "")), "\\s+").alias("words"), col("filename"))

# Remove stop words and words of length shorter than 3
remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
remover.loadDefaultStopWords("english")
filtered_df = remover.transform(words_df)

# Explode the filtered words into individual rows
filtered_words_df = filtered_df.select(explode(col("filtered_words")).alias("word"), col("filename"))
filtered_words_df = filtered_words_df.filter(length(col("word")) >= 3)

# Compute term frequency (TF)
hashing_tf = HashingTF(inputCol="filtered_words", outputCol="raw_features", numFeatures=10000)
featurized_data = hashing_tf.transform(filtered_df)

# Compute inverse document frequency (IDF)
idf = IDF(inputCol="raw_features", outputCol="features")
idf_model = idf.fit(featurized_data)
rescaled_data = idf_model.transform(featurized_data)

# Extract TF-IDF scores
def extract_values(v):
    return v.values.tolist()

extract_values_udf = spark.udf.register("extract_values", extract_values, "array<double>")

tfidf_scores = rescaled_data.select(explode(col("filtered_words")).alias("word"), explode(extract_values_udf(col("features"))).alias("score"))

# Sum the TF-IDF scores for each word
tfidf_scores = tfidf_scores.groupBy("word").sum("score").orderBy("sum(score)", ascending=False)

# Get the 20 words with the highest TF-IDF scores
top_words = tfidf_scores.limit(20).collect()

# Convert to dictionary for word cloud
word_freq = {row['word']: row['sum(score)'] for row in top_words}

# Generate word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# Stop Spark session
spark.stop()