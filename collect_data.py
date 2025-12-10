import os
import json
import re
import csv

# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------
CASES_DIR = "./data/cases"
OUTPUT = "./data/cases.json"
JUSTICE_CSV = "./data/justice.csv"

transcript_pattern = re.compile(r".*[-_][tT]\d+\.json$")

cases = {}

# -------------------------------------------------------
# HELPERS
# -------------------------------------------------------
def clean_text(text):
    """Strip HTML tags, normalize whitespace."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -------------------------------------------------------
# LOAD justice.csv INTO LOOKUP BY HREF
# -------------------------------------------------------
justice_data = {}
with open(JUSTICE_CSV, "r", encoding="utf-8") as jf:
    reader = csv.DictReader(jf)
    for row in reader:
        href = row["href"].strip()
        justice_data[href] = row

print("Loaded justice.csv:", len(justice_data), "rows")


# -------------------------------------------------------
# FIRST PASS — LOAD ALL BASE CASE FILES
# -------------------------------------------------------
for fname in os.listdir(CASES_DIR):
    if not fname.endswith(".json"):
        continue
    if transcript_pattern.match(fname):
        continue  # skip transcript files

    path = os.path.join(CASES_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    href = data.get("href", "").strip()

    # ---------------------------
    # MATCH BASE CASE TO CSV
    # ---------------------------
    if href not in justice_data:
        cases[fname] = {"skip_reason": "no_csv_match", "href": href}
        continue

    row = justice_data[href]

    # Parse first_party_winner from CSV
    fpw_raw = row.get("first_party_winner", "").strip().lower()
    if fpw_raw in ("true", "1", "yes"):
        winner = True
    elif fpw_raw in ("false", "0", "no"):
        winner = False
    else:
        cases[fname] = {"skip_reason": "winner_missing_csv"}
        continue

    # Clean facts
    facts = clean_text(row.get("facts", ""))

    cases[fname] = {
        "href": href,
        "case_name": row.get("name"),
        "year": row.get("term"),

        "first_party": clean_text(row.get("first_party", "")),
        "second_party": clean_text(row.get("second_party", "")),
        "facts": facts,
        "decision": winner,

        "docket": row.get("docket"),
        "facts_len": row.get("facts_len"),
        "majority_vote": row.get("majority_vote"),
        "minority_vote": row.get("minority_vote"),
        "decision_type": row.get("decision_type"),
        "disposition": row.get("disposition"),
        "issue_area": row.get("issue_area"),

        "transcript_parts": [],
        "has_transcript": False
    }

print("Collected Cases")


# -------------------------------------------------------
# SECOND PASS — LOAD TRANSCRIPTS
# -------------------------------------------------------
for fname in os.listdir(CASES_DIR):
    if not fname.endswith(".json"):
        continue
    if not transcript_pattern.match(fname):
        continue

    base_name = re.sub(r"[-_][tT]\d+\.json$", ".json", fname)

    if base_name not in cases:
        continue
    if "skip_reason" in cases[base_name]:
        continue

    tpath = os.path.join(CASES_DIR, fname)
    with open(tpath, "r", encoding="utf-8") as f:
        tdata = json.load(f)

    transcript = tdata.get("transcript", {})
    if not transcript:
        continue

    collected = []
    for section in transcript.get("sections", []):
        for turn in section.get("turns", []):
            for block in turn.get("text_blocks", []):
                txt = block.get("text", "").replace("\n", " ").strip()
                if txt:
                    collected.append(txt)

    full_text = " ".join(collected).strip()
    if full_text:
        cases[base_name]["has_transcript"] = True
        cases[base_name]["transcript_parts"].append(full_text)

print("Transcript loading complete.")


# -------------------------------------------------------
# SUMMARY STATISTICS BEFORE FINAL OUTPUT
# -------------------------------------------------------
total_base_files = len(cases)
total_transcript_files = sum(
    1 for f in os.listdir(CASES_DIR) if transcript_pattern.match(f)
)

# -------------------------------------------------------
# BUILD FINAL OUTPUT JSON
# -------------------------------------------------------
output_obj = {
    "cases": [],
    "skipped": 0,
    "stats": {
        "total_base_case_files": total_base_files,
        "total_transcript_files": total_transcript_files
    }
}

for key, row in sorted(cases.items()):
    if "skip_reason" in row or not row["has_transcript"]:
        output_obj["skipped"] += 1
        continue

    transcript_text = " ".join(row["transcript_parts"])

    output_obj["cases"].append({
        "case_name": row["case_name"],
        "href": row["href"],
        "year": row["year"],
        "first_party": row["first_party"],
        "second_party": row["second_party"],
        "decision": row["decision"],
        "facts": row["facts"],
        "transcript": transcript_text
    })


# Winner-ratio diagnostic
winner_first = sum(1 for c in output_obj.values()
                   if isinstance(c, dict)
                   and "decision" in c
                   and c["decision"] is True)

winner_second = sum(1 for c in output_obj.values()
                    if isinstance(c, dict)
                    and "decision" in c
                    and c["decision"] is False)

# -------------------------------------------------------
# WRITE OUTPUT
# -------------------------------------------------------
with open(OUTPUT, "w", encoding="utf-8") as out:
    json.dump(output_obj, out, indent=2, ensure_ascii=False)

# -------------------------------------------------------
# FINAL PRINTS
# -------------------------------------------------------
print("Final base case files:", total_base_files)
print("Total transcript files:", total_transcript_files)
print("Final cases included:", len(output_obj["cases"]))
print("Cases skipped:", output_obj["skipped"])
print("Wrote JSON to:", OUTPUT)
