# 🏥 Healthcare Data QA Pipeline (ETL Validator)

## 📌 Overview
In the healthcare and health-tech industries, raw data provided by hospital systems or legacy databases is frequently incomplete, improperly formatted, or corrupted. If this "dirty" data enters a production database, it can crash analytics dashboards or cause billing systems to fail.

This project is a **Data Quality Assurance (QA) pipeline** built in Python. It acts as the first line of defense in an Extract, Transform, Load (ETL) process. It ingests medical billing records (CSV), performs strict schema and content validation using Pandas, and generates a detailed audit report of any records that violate business logic.

## 🚀 Key Features

* **Schema Validation ("The Bouncer"):** Instantly rejects files that are missing required columns or contain unexpected "junk" columns before any processing occurs.
* **Content Validation ("The Rules Engine"):** Iterates through records applying strict domain constraints using defensive programming. 
  * Safely handles `NaN` values and empty strings.
  * Cleans and verifies financial data (e.g., stripping symbols and ensuring `BASE_COST` and `PAYER_COVERAGE` are non-negative numbers).
  * Enforces logical constraints (e.g., ensuring active prescriptions without a `STOP` date do not crash the parser).
* **Detailed Audit Reporting:** Instead of failing silently or crashing, the script logs exactly which rows and patient IDs failed, and specifically which rules were violated.

## 🛠️ Technologies Used
* **Python 3.x**
* **Pandas** (Data ingestion and null-value handling)

## 🧠 How it Works

The pipeline executes in two distinct phases:

1. **Phase 1 (Schema Check):** The `validate()` function reads the CSV headers. It compares the actual columns against a hardcoded list of `required_keys`. If the sets do not match perfectly, the pipeline halts immediately.
2. **Phase 2 (Content Check):** The `find_invalid_records()` function extracts the data as a list of dictionaries. It uses a dynamic `constraints` dictionary to evaluate every single cell against predefined rules, catching bad data types and negative financial values.

## 📊 Sample Output

When running the pipeline against a dirty dataset, the terminal generates an easy-to-read audit report:
```text
Initiating Medical Data Validator...
----------------------------------------
✅ Schema Validation: Passed (Format is correct)
⏳ Content Validation: Scanning records...

⚠️ AUDIT FAILED: Found 3 invalid records:
  -> Row 4850 (Patient 95f186d2-2d83-20c7-df20-0ce6777098e1) Failed: ['CODE']
  -> Row 5181 (Patient 95f186d2-2d83-20c7-df20-0ce6777098e1) Failed: ['PAYER_COVERAGE', 'CODE']
  -> Row 5360 (Patient 7adec7c5-56a4-f1a1-1720-c5e880ae07a5) Failed: ['STOP', 'CODE', 'PAYER_COVERAGE']
