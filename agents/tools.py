"""
Tools available to the Clinical Trial Safety Analyzer agents.
Each tool is a plain Python function decorated with @tool.
The docstring is what the LLM reads to decide when and how to call it.
"""
from langchain_core.tools import tool


@tool
def calculate_severity_score(event_description: str) -> dict:
    """Calculate a numerical severity score (1-10) for an adverse event description.

    Args:
        event_description: Free-text description of the adverse event or outcome.
    """
    severity_map = {
        "death": 10, "fatal": 10,
        "life-threatening": 9,
        "hospitalized": 7, "hospitalization": 7, "serious": 7, "severe": 7,
        "moderate": 5, "significant": 5,
        "mild": 2, "minor": 2, "slight": 1,
    }
    text = event_description.lower()
    best_score, best_term = 1, "unspecified"
    for term, score in severity_map.items():
        if term in text and score > best_score:
            best_score, best_term = score, term
    return {"score": best_score, "matched_term": best_term, "scale": "1–10"}


@tool
def lookup_drug_class(drug_name: str) -> str:
    """Look up the pharmacological class of a drug by name.

    Args:
        drug_name: The name of the drug (generic name preferred).
    """
    db = {
        "metformin": "Biguanide / Antidiabetic",
        "aspirin": "NSAID / Antiplatelet",
        "warfarin": "Anticoagulant",
        "lisinopril": "ACE Inhibitor / Antihypertensive",
        "atorvastatin": "Statin / Lipid-lowering agent",
        "amoxicillin": "Penicillin / Antibiotic",
        "ibuprofen": "NSAID / Analgesic",
        "omeprazole": "Proton Pump Inhibitor",
    }
    result = db.get(drug_name.lower())
    if result:
        return f"{drug_name.title()}: {result}"
    return f"Drug class for '{drug_name}' not found in local database."


@tool
def check_required_fields(report_text: str) -> dict:
    """Check whether an adverse event report contains all ICH E2B required fields.

    Args:
        report_text: The full text of the adverse event report.
    """
    required = {
        "patient":       ["patient", "age", "subject", "year-old"],
        "drug":          ["drug", "medication", "compound", "mg"],
        "onset_date":    ["onset", "date", "started", "began"],
        "adverse_event": ["adverse event", "reaction", "side effect", "symptom", "nausea", "vomiting", "pain"],
        "outcome":       ["outcome", "resolved", "hospitalized", "recovered", "death", "ongoing"],
        "reporter":      ["reporter", "physician", "investigator", "reported by", "prescribing"],
    }
    text = report_text.lower()
    results = {field: any(kw in text for kw in keywords) for field, keywords in required.items()}
    missing = [f for f, found in results.items() if not found]
    return {
        "fields_present": results,
        "complete": len(missing) == 0,
        "missing_fields": missing,
    }
