# =========================
# IMPORT LIBRARIES
# =========================
import pandas as pd
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer

# =========================
# LOAD DATASET (RAJAH 3.1 & 3.2)
# =========================
print("===== RAJAH 3.1 & 3.2: LOAD DATASET =====")

# Correct path (your dataset inside data folder)
df = pd.read_csv("data/passive_dataset.csv")

print("\n--- Dataset Preview ---")
print(df.head())

print("\n--- Column Names ---")
print(df.columns)

# =========================
# EDA GRAPH (RAJAH 3.3)
# =========================
print("\n===== RAJAH 3.3: CLASS DISTRIBUTION =====")

df['label'].value_counts().plot(kind='bar')
plt.title("Taburan Kategori Mesej")
plt.xlabel("Kategori")
plt.ylabel("Bilangan")
plt.show()

# =========================
# CLEANING (RAJAH 3.4)
# =========================
print("\n===== RAJAH 3.4: DATA CLEANING =====")

# Take one sample
sample = df['text'][0]

# Simple cleaning
cleaned = sample.lower()

print("\nBefore Cleaning:")
print(sample)

print("\nAfter Cleaning:")
print(cleaned)

# =========================
# BALANCING CHECK (RAJAH 3.5)
# =========================
print("\n===== RAJAH 3.5: CLASS BALANCING =====")

print(df['label'].value_counts())

# =========================
# EMBEDDING (RAJAH 3.6)
# =========================
print("\n===== RAJAH 3.6: SENTENCE EMBEDDING =====")

model = SentenceTransformer('all-MiniLM-L6-v2')

test_sentence = "Saya tunggu dari pagi lagi"
vector = model.encode(test_sentence)

print("\nSample Sentence:")
print(test_sentence)

print("\nVector (first 10 values):")
print(vector[:10])

print("\n===== DONE =====")