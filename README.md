# 🩺 Physician Notetaker – NLP Pipeline

An end-to-end **NLP-based medical transcription processor** that extracts structured medical information, analyzes patient sentiment & intent, and generates a SOAP note from physician–patient conversations.

This project demonstrates **AI reasoning, NLP pipeline design, and clean engineering practices** without relying on external API keys.

---

## 📌 Features

- Reads physician–patient transcripts from **.txt** or **.docx** files  
- Extracts **key medical details** in structured JSON format  
- Performs **patient sentiment & intent analysis**  
- Automatically generates a **SOAP clinical note**  
- Outputs a **single consolidated JSON report**  
- No API key required (mock LLM responses used)

---

## 🧠 NLP Pipeline Overview

The pipeline consists of three main AI agents:

1. **Medical Information Extraction**
   - Patient Name
   - Symptoms
   - Diagnosis
   - Treatment
   - Current Status
   - Prognosis

2. **Sentiment & Intent Analysis**
   - Sentiment: Anxious / Neutral / Reassured
   - Intent: Reporting symptoms / Seeking reassurance / Expressing concern / Other

3. **SOAP Note Generation**
   - Subjective
   - Objective
   - Assessment
   - Plan

All outputs are combined into a single structured JSON object.

---

## 📂 Project Structure

.
├── code file.py
├── sample transcript.txt        (optional)
└── README.md

---

## ⚙️ Installation

1. Clone the repository
   git clone <repository-url>
   cd physician-notetaker

2. Install dependencies
   pip install python-docx python-dotenv

---

## ▶️ Usage

Run the script using a transcript file:

python code\ file.py --file path/to/transcript.txt

---

## 📤 Output

The script prints a formatted JSON output containing:
- Medical Summary
- Sentiment & Intent
- SOAP Note

---

## 🧪 Design Notes

- Mock LLM responses are used to avoid external API dependencies
- Modular design allows easy replacement with real LLM APIs
- Clear separation of concerns for maintainability

---

## 🚀 Future Improvements

- Integrate real LLM APIs
- Add Named Entity Recognition (NER)
- Support multiple languages
- Export to PDF or EHR formats

---

## 👨‍💻 Author

Ashish Khatri  
B.Tech CSE (AI & ML)

---

## 📄 License

For educational and evaluation purposes only.
