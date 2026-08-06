# ToneFix AI

> An AI-powered passive-aggressive message detection system using Machine Learning and Natural Language Processing (NLP).

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-SVM-orange)
![Sentence Transformers](https://img.shields.io/badge/Sentence%20Transformers-NLP-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20Application-red?logo=streamlit)

---

## 📖 Overview

ToneFix AI is a machine learning-based web application that detects passive-aggressive communication in text messages. The system analyzes user input and classifies the message into one of three categories: **Positive**, **Neutral**, or **Passive-Aggressive**.

The application applies Natural Language Processing (NLP) techniques using **Sentence Transformers** for text embeddings and a **Support Vector Machine (SVM)** classifier to identify communication tone. The goal is to help users recognize potentially negative communication patterns and encourage clearer, more effective written communication.

This project was developed as a **Final Year Project (FYP)** for the **Bachelor of Computer Science (Artificial Intelligence)** programme at **Universiti Kebangsaan Malaysia (UKM)**.

---

## ✨ Features

- 🔍 Detects passive-aggressive communication in text
- 😊 Classifies messages into:
  - Positive
  - Neutral
  - Passive-Aggressive
- 🧠 Machine learning-based text classification using Support Vector Machine (SVM)
- 📊 Displays prediction confidence
- 📝 Maintains message history
- ⚡ Interactive web application built with Streamlit

---

## 🛠 Technologies Used

- Python
- Streamlit
- Sentence Transformers
- Scikit-learn
- Support Vector Machine (SVM)
- Pandas
- NumPy

---

## 📂 Project Structure

```text
ToneFix-AI/
│
├── data/                  # Dataset
├── model/                 # Trained machine learning model
├── app.py                 # Main Streamlit application
├── train.py               # Train the classification model
├── make_dataset.py        # Dataset preparation
├── test_app.py            # Application testing
├── test_data.py           # Dataset testing
├── requirements.txt       # Required Python packages
├── .gitignore
└── README.md
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/iamdarvin12/ToneFix-AI.git
```

Navigate to the project directory:

```bash
cd tonefix-ai
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Launch the Streamlit application:

```bash
streamlit run app.py
```

---

## 🧠 Training the Model

To retrain the machine learning model:

```bash
python train.py
```


## Trained Model

The trained model is not included in this repository because it exceeds GitHub's file size limit.

To generate the model, run:

```bash
python train.py
```

The trained model will be saved in the `model/` directory.
---

## 🧪 Running Tests

Run the application tests:

```bash
python test_app.py
```

Run the dataset tests:

```bash
python test_data.py
```

---

## 📊 System Workflow

1. User enters a text message.
2. The text is preprocessed.
3. Sentence embeddings are generated.
4. The trained SVM model predicts the communication tone.
5. The application displays the predicted category together with the confidence score.

---




## 📄 License

This project is developed for educational and research purposes.

---

## 👨‍💻 Author

**DARVIN A/L BATHUMALY**

Bachelor of Computer Science (Artificial Intelligence)

Faculty of Information Science and Technology (FTSM)

Universiti Kebangsaan Malaysia (UKM)

---

## 🙏 Acknowledgements

- Universiti Kebangsaan Malaysia (UKM)
- Sentence Transformers
- Scikit-learn
- Streamlit
- Python Open Source Community