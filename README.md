# 🏥 Healthcare Data QA Pipeline (ETL Validator)

## 🎓 Background & Inspiration
This project was built following the concepts introduced in the [freeCodeCamp "Build a Medical Data Validator" tutorial](https://www.youtube.com/watch?v=GetPPXviwUo). 

However, instead of validating hardcoded, perfectly clean Python lists (as done in the tutorial), I took the foundational logic and engineered it to process **real-world, messy CSV datasets**. By integrating **Pandas**, this script acts as a true Data Quality Assurance (QA) pipeline, anticipating and gracefully handling missing values, corrupted strings, and unexpected data types.

## 📌 Overview
In the healthcare and health-tech industries, raw data provided by hospital systems or legacy databases is frequently incomplete. If "dirty" data enters a production database, it can crash downstream analytics or cause billing systems to fail.

This Python script (`Medical Data Validator.py`) acts as the first line of defense in an Extract, Transform, Load (ETL) process. It ingests medical billing records, performs strict schema and content validation, and generates a detailed terminal audit report of any records that violate medical business logic.

## 📂 Data Source
The dataset used to test this pipeline (`medications.csv`) was generated using [**Synthea™**](https://synthetichealth.github.io/synthea/), an open-source synthetic patient population simulator. Using Synthea provides a highly realistic, complex healthcare dataset to test ETL logic while ensuring all patient records are 100% synthetic and HIPAA compliant.

## 🚀 Key Features

* **Schema Validation ("The Bouncer"):** Instantly rejects files that are missing required columns or contain unexpected "junk" columns before any processing occurs.
* **Content Validation ("The Rules Engine"):** Iterates through records applying strict domain constraints using defensive programming. 
  * Safely handles `NaN` values and empty strings.
  * Cleans and verifies financial data (e.g., stripping symbols and ensuring `BASE_COST` and `PAYER_COVERAGE` are non-negative numbers).
  * Enforces logical constraints (e.g., ensuring active prescriptions without a `STOP` date do not crash the parser).
* **Detailed Audit Reporting:** Instead of crashing when encountering bad data, the script logs exactly which rows failed and specifically which rules were violated.

## 📊 Sample Output

When running the pipeline against a dirty dataset, the terminal generates an easy-to-read audit report. Here is an example of the script catching missing codes and invalid payer coverage amounts:
```text
Initiating Medical Data Validator...
----------------------------------------
✅ Schema Validation: Passed (Format is correct)
⏳ Content Validation: Scanning records...

⚠️ AUDIT FAILED: Found invalid records:
  -> Row 4850 (Patient 95f186d2-2d83-20c7-df20-0ce6777098e1) Failed: ['CODE']
  -> Row 4852 (Patient 95f186d2-2d83-20c7-df20-0ce6777098e1) Failed: ['STOP', 'CODE', 'PAYER_COVERAGE']
  -> Row 5181 (Patient 95f186d2-2d83-20c7-df20-0ce6777098e1) Failed: ['CODE', 'PAYER_COVERAGE']
  -> Row 5360 (Patient 7adec7c5-56a4-f1a1-1720-c5e880ae07a5) Failed: ['STOP', 'CODE', 'PAYER_COVERAGE']
  -> Row 5824 (Patient dd0b60d1-bb3c-0e88-a070-ff083161ce31) Failed: ['STOP', 'CODE']
