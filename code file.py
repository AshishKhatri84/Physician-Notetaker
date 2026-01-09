import os
import json
import re
import argparse
from docx import Document
from dotenv import load_dotenv

# --------------------------------------------------
# Config
# --------------------------------------------------

load_dotenv()

ALLOWED_EXTENSIONS = {"txt", "docx"}

# --------------------------------------------------
# Utils
# --------------------------------------------------

def call_llm(prompt: str) -> str:
    # Mock responses for demonstration without API key
    if "medical details" in prompt.lower():
        return '{"Patient_Name": "John Doe", "Symptoms": ["headache", "nausea", "dizziness"], "Diagnosis": "Migraine", "Treatment": "Pain relievers and rest", "Current_Status": "Stable", "Prognosis": "Good with treatment"}'
    elif "sentiment" in prompt.lower() and "intent" in prompt.lower():
        return '{"Sentiment": "Anxious", "Intent": "Reporting symptoms"}'
    elif "soap note" in prompt.lower():
        return '{"Subjective": "Patient reports headache, nausea, and dizziness for 2 days.", "Objective": "Vital signs normal.", "Assessment": "Possible migraine.", "Plan": "Prescribe medication and follow up."}'
    else:
        return '{"error": "Unknown prompt type"}'


def clean_json(text: str) -> str:
    return re.sub(r"```json|```", "", text).strip()


def parse_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON output"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def read_file(file_path):
    if file_path.endswith(".txt"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None

    if file_path.endswith(".docx"):
        try:
            doc = Document(file_path)
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception:
            return None

    return None

# --------------------------------------------------
# AI Agents
# --------------------------------------------------

def medical_summarize(transcript: str) -> dict:
    prompt = (
        "Extract key medical details from this physician-patient conversation "
        "and output JSON with:\n"
        "- Patient_Name\n"
        "- Symptoms (list)\n"
        "- Diagnosis\n"
        "- Treatment\n"
        "- Current_Status\n"
        "- Prognosis\n"
        "Set missing fields to 'Not specified'.\n\n"
        f"Transcript:\n{transcript}"
    )

    response = clean_json(call_llm(prompt))
    return parse_json(response)


def analyze_sentiment_intent(transcript: str) -> dict:
    prompt = (
        "Analyze the patient's sentiment (Anxious, Neutral, Reassured) "
        "and intent (Seeking reassurance, Reporting symptoms, Expressing concern, Other). "
        "Return JSON with keys: Sentiment, Intent.\n\n"
        f"Transcript:\n{transcript}"
    )

    response = clean_json(call_llm(prompt))
    return parse_json(response)


def generate_soap_note(transcript: str) -> dict:
    prompt = (
        "Generate a SOAP note with:\n"
        "- Subjective\n"
        "- Objective\n"
        "- Assessment\n"
        "- Plan\n"
        "Set missing fields to 'Not specified'. Return JSON.\n\n"
        f"Transcript:\n{transcript}"
    )

    response = clean_json(call_llm(prompt))
    return parse_json(response)


def combine_outputs(medical_summary, sentiment_intent, soap_note) -> dict:
    return {
        "Medical_Summary": medical_summary,
        "Sentiment_Intent": sentiment_intent,
        "SOAP_Note": soap_note,
    }

# --------------------------------------------------
# Main Processing
# --------------------------------------------------

# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process physician-patient transcript and generate medical summary, sentiment analysis, and SOAP note.")
    parser.add_argument("--file", required=True, help="Path to the transcript file (.txt or .docx)")
    args = parser.parse_args()

    file_path = args.file

    if not os.path.exists(file_path):
        print(json.dumps({"error": "File does not exist"}))
        exit(1)

    if not allowed_file(file_path):
        print(json.dumps({"error": "Unsupported file type. Only .txt and .docx are allowed"}))
        exit(1)

    text = read_file(file_path)
    if not text:
        print(json.dumps({"error": "Failed to read file"}))
        exit(1)

    medical_summary = medical_summarize(text)
    sentiment_intent = analyze_sentiment_intent(text)
    soap_note = generate_soap_note(text)

    result = combine_outputs(medical_summary, sentiment_intent, soap_note)

    print(json.dumps(result, indent=4))