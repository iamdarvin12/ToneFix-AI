import pandas as pd
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

print("Loading dataset...")
df = pd.read_csv("data/passive_dataset.csv")

# Clean
df = df.dropna()
df["text"] = df["text"].astype(str).str.strip()
df["label"] = df["label"].astype(str).str.strip().str.lower()

print("\nDataset size:", len(df))
print("\nClass balance:\n", df["label"].value_counts())

# Load embedding model
print("\nLoading embedding model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Encode text
print("\nEncoding text...")
X = embedder.encode(df["text"].tolist(), show_progress_bar=True)
y = df["label"].tolist()

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
print("\nTraining model...")
model = SVC(kernel="linear", probability=True)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nReport:\n", classification_report(y_test, y_pred))

# Save
joblib.dump(model, "model/tone_model.pkl")
joblib.dump(embedder, "model/embedder.pkl")

print("\nModel saved successfully!")