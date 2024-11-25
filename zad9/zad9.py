from pyspark.sql import SparkSession
from pyspark.ml.feature import StopWordsRemover
from pyspark.sql.functions import regexp_replace, split, explode, col, length

# Inicjalizacja sesji Spark
spark = SparkSession.builder.appName("ShakespeareAnalysis").getOrCreate()

# Wczytanie pliku tekstowego
file_path = "zad9/shakespear/hamlet.txt"  # Podaj właściwą ścieżkę do pliku
raw_data = spark.read.text(file_path)


# Usunięcie zbędnych znaków, takich jak interpunkcja
cleaned_data = raw_data.withColumn("words", split(regexp_replace("value", "[^\\w\\s]", ""), "\\s+"))

# Step 1: Split lines into arrays of words (keeping them in array format for StopWordsRemover)
cleaned_data = raw_data.withColumn("words", split(regexp_replace("value", "[^\\w\\s]", ""), "\\s+"))

# Step 2: Apply StopWordsRemover (expects array<string> input)
remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
filtered_words_array = remover.transform(cleaned_data)

# Step 3: Flatten the array and remove short words
filtered_words = filtered_words_array.select(explode(col("filtered_words")).alias("word")) \
                                     .filter(length(col("word")) > 2)

# Usuń słowa o długości <= 2
filtered_words = filtered_words.filter(filtered_words.filtered_word.rlike(r"^.{3,}$"))

# Zliczanie częstotliwości słów
word_counts = filtered_words.groupBy("filtered_word").count()

# Zmiana formatu na Pandas DataFrame, aby łatwiej użyć wordcloud
word_counts_pd = word_counts.toPandas()

# Importowanie wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Przygotowanie słownika słów dla wordcloud
word_freq_dict = dict(zip(word_counts_pd["filtered_word"], word_counts_pd["count"]))

# Generowanie chmury wyrazów
wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_freq_dict)

# Wyświetlenie chmury wyrazów
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
