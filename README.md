<<<<<<< HEAD
# Clinical Note Summariser

An AI-powered clinical decision support tool that analyses free-text clinical notes and returns structured summaries, key findings, risk flags, and recommended actions.

Built with FastAPI and the Anthropic Claude API. Designed to demonstrate the intersection of biomedical domain knowledge and modern AI engineering.

**[Live demo →](https://clinical-note-summariser.onrender.com)**

![Python](https://img.shields.io/badge/Python-3.12-3776ab?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Anthropic](https://img.shields.io/badge/Claude_API-Anthropic-d4a574)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Deployed on Render](https://img.shields.io/badge/Deployed_on-Render-46e3b7?logo=render&logoColor=white)

---

## What it does

Clinicians deal with large volumes of unstructured notes — referral letters, discharge summaries, ward handover documentation. Reading and mentally parsing these is time-consuming and error-prone, especially under fatigue.

This tool accepts a raw clinical note and returns:

- **Summary** — a plain-English overview of the patient presentation
- **Key findings** — the clinically significant details extracted from the note
- **Risk flags** — potential safety concerns categorised by type and severity (high / medium / low)
- **Recommended actions** — suggested next steps based on the clinical picture

The analysis is powered by Claude's tool use feature, which returns structured JSON rather than free-text — ensuring consistent, parseable output that integrates cleanly with downstream systems.

## Who would use this

- **Junior doctors** doing ward handovers who need a quick structured overview of an unfamiliar patient
- **GPs** reviewing referral letters or discharge summaries from secondary care
- **Nurses** triaging incoming clinical documentation
- **Clinical coders** extracting diagnoses and procedures from notes for hospital records
- **Medical students** learning to identify the key elements in a clinical note

## How it works

```
Clinical note (free text)
        │
        ▼
   FastAPI endpoint (/summarise)
        │
        ▼
   Claude API (tool use)
   ┌─────────────────────────┐
   │ System prompt with       │
   │ clinical decision support│
   │ persona + structured     │
   │ output schema            │
   └─────────────────────────┘
        │
        ▼
   Pydantic validation
        │
        ▼
   Structured JSON response
   (summary, findings, risks, actions)
```

The system prompt instructs Claude to act as a clinical decision support assistant. A tool schema defines the exact output structure — `summary`, `key_findings`, `risk_flags` (with `category`, `detail`, `severity`), and `recommended_actions`. Claude is forced to use this tool via `tool_choice`, which eliminates free-text variability and ensures every response conforms to the expected shape.

## Example

**Input:**
```json
{
  "note": "68F presenting with chest tightness and shortness of breath onset 2hrs ago. Hx: T2DM on Metformin, hypertension on Lisinopril. Scheduled CT with contrast tomorrow. SpO2 92% on room air. BP 158/94. Bilateral crackles on auscultation.",
  "patient_age": 68,
  "patient_sex": "female"
}
```

**Output:**
```json
{
  "summary": "68-year-old female presenting with acute onset chest tightness and shortness of breath with hypoxia and bilateral crackles, suggesting possible acute pulmonary edema or decompensated heart failure.",
  "key_findings": [
    "SpO2 92% on room air — clinically significant hypoxia",
    "BP 158/94 mmHg — uncontrolled hypertension",
    "Bilateral crackles — suggestive of pulmonary edema"
  ],
  "risk_flags": [
    {
      "category": "medication",
      "detail": "Metformin must be held before and 48 hours after iodinated contrast CT due to risk of lactic acidosis",
      "severity": "high"
    },
    {
      "category": "vital_signs",
      "detail": "SpO2 92% on room air indicates hypoxia requiring immediate supplemental oxygen",
      "severity": "high"
    }
  ],
  "recommended_actions": [
    "Initiate supplemental oxygen immediately to target SpO2 ≥ 95%",
    "Hold Metformin immediately given planned contrast CT",
    "Obtain urgent 12-lead ECG to rule out ACS"
  ]
}
```

## Tech stack

| Layer          | Technology                          |
|----------------|-------------------------------------|
| Backend        | Python 3.12, FastAPI                |
| AI             | Anthropic Claude API (tool use)     |
| Data validation| Pydantic v2                         |
| Frontend       | Vanilla HTML/CSS/JS                 |
| Containerisation| Docker                             |
| Deployment     | Render                              |

## Running locally

```bash
git clone https://github.com/ThomasWaugh/clinical-note-summariser.git
cd clinical-note-summariser
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
uvicorn app.main:app --reload
```

Open `http://localhost:8000` for the web interface, or `http://localhost:8000/docs` for the interactive API docs.

**With Docker:**
```bash
docker build -t clinical-note-summariser .
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=your-key-here clinical-note-summariser
```

## Project structure

```
clinical-note-summariser/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app + routes
│   ├── summariser.py         # Claude API integration + tool schema
│   ├── models.py             # Pydantic request/response models
│   └── static/
│       └── index.html        # Frontend interface
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
```

## Limitations and responsible use

This tool is designed as a **decision support aid**, not a replacement for clinical judgement. There are important limitations to understand:

**Accuracy is not guaranteed.** The underlying language model can occasionally hallucinate details that were not present in the original note, miss subtle but clinically significant information, or misjudge the severity of a finding. Output should always be verified against the source note.

**No access to full patient context.** The model only sees the text provided in a single note. It has no access to the patient's full medical history, medication records, lab trends, imaging, or prior consultations. A human clinician integrates all of these when making decisions — this tool cannot.

**Not a diagnostic tool.** The summaries and risk flags reflect pattern recognition in the input text, not clinical reasoning. The model does not understand pathophysiology in the way a trained clinician does. It may identify risks correctly without understanding why they matter, or miss risks that require inference across multiple data points.

**Not validated for clinical use.** This tool has not undergone clinical validation, regulatory review, or testing against established clinical decision support standards. It is a portfolio demonstration project, not a medical device.

**LLM outputs can vary.** Even with identical input, the model may produce slightly different outputs across requests. The tool use schema constrains the structure but not the clinical content of the response.

The frontend includes a disclaimer: *"For decision support only — always verify findings with clinical judgement."* This reflects the intended positioning of the tool.

## Background

Built by [Tom Waugh](https://linkedin.com/in/tomwaugh-msc) as part of a health tech AI portfolio. The biomedical domain knowledge embedded in the prompt design — T2DM management, contrast contraindications, anticoagulation decisions, vital sign interpretation — comes from a Human Biology & Infectious Disease background, not generic summarisation.

## Licence

MIT
=======
# Council Swimming Analytics

A suite of interactive data tools built for **West Lancashire Borough Council** to analyse weekly swimming lesson performance across two sites — **Park Pool** and **Nye Bevan**.

Built and delivered end-to-end: from raw weekly booking CSV exports to council-ready management dashboards, currently in active use and being presented to the local council.

---

## Tools

### 🔄 Weekly Analyser (`swimming_weekly_analyser.html`)
The core tool. Drop in any weekly bookings CSV and it instantly generates a full performance report — no server, no login, no setup required.

**Produces automatically:**
- Combined summary across both pools
- Park Pool vs Nye Bevan side-by-side comparison
- Capacity utilisation breakdown (green / amber / red)
- Fill rate by stage, sorted best to worst
- Under-utilised classes flagged (<50% full)
- Teacher workload and average fill rate

**[▶ Try it live](https://thomasjdwaugh.github.io/council-swimming-analytics/swimming_weekly_analyser.html)**

---

### 🏊 Park Pool Dashboard (`park_pool_dashboard.html`)
Detailed lesson-level view for Park Pool — 130 group lessons, filterable by day, stage, teacher, and class name. Shows bookings, capacity, and fill rate per lesson.

### 🏊 Nye Bevan Dashboard (`nye_bevan_dashboard.html`)
Same dashboard for Nye Bevan — 63 lessons across 5 teachers with full fill rate breakdown.

### 📊 Council Insights Dashboard (`council_insights_dashboard.html`)
Executive summary built for council presentation — pool comparison, capacity utilisation buckets, stage-level fill rates, and a flagged list of under-utilised classes requiring action.

---

## How It Works

All tools are **standalone HTML files** — no backend, no dependencies, no installation. They run entirely in the browser using vanilla JavaScript.

The weekly analyser reads the CSV client-side, infers teachers from class names, filters private 1-2-1 lessons automatically, and renders the full dashboard in under a second.

**Expected CSV columns:**
```
Description | Class Name | Class Date Time | Bookings | Class Size | % Uptake | Income
```

---

## Stack

`HTML` · `CSS` · `Vanilla JavaScript` · `CSV parsing` · `GitHub Pages`

---

## Context

This project was built alongside my role as a Lifeguard/Gym Instructor at West Lancashire Borough Council. Management needed a way to identify underperforming lessons — classes with low fill rates, imbalanced teacher workloads, and capacity being wasted — without relying on manual spreadsheet analysis each week.

The result is a zero-dependency, self-service reporting tool that any non-technical manager can use by dragging and dropping a CSV file. The insights generated are now being used to make operational timetabling decisions and are being presented directly to the council.

---

## Author

**Thomas Waugh** — AI Engineer · MSc Data Science · BSc Human Biology & Infectious Disease

[GitHub](https://github.com/ThomasJDWaugh) · [LinkedIn](https://linkedin.com/in/tomwaugh-msc)# council-swimming-analytics
>>>>>>> ad60acb943b11897efefd221bc47ee287530ad94
