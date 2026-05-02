import pandas as pd

filename = r"C:\Users\truon\OneDrive\Pictures\Medical Data Validator\medications.csv"
required_keys = [
    "START", "STOP", "PATIENT", "PAYER", "ENCOUNTER", "CODE", 
    "DESCRIPTION", "BASE_COST", "PAYER_COVERAGE", "DISPENSES", 
    "TOTALCOST", "REASONCODE", "REASONDESCRIPTION"
]


def validate(file_path):
    """Loads the CSV and ensures ONLY required columns exist."""
    try:
        df = pd.read_csv(file_path)
        
        actual_columns = df.columns.tolist()
        
        missing = set(required_keys) - set(actual_columns)
        if missing:
            print(f"Error: Missing required columns: {missing}")
            return False
            
        extra = set(actual_columns) - set(required_keys)
        if extra:
            print(f"Error: Invalid Format. Extra unknown columns detected: {extra}")
            return False
        df = df[required_keys]
        medical_records = df.to_dict('records')
        return medical_records
        
    except FileNotFoundError:
        print(f"Error: Could not find '{file_path}'.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def find_invalid_records(records):
    bad_rows = []
    
    for index, record in enumerate(records):
        raw_coverage = record.get("PAYER_COVERAGE")
        
        is_empty_coverage = pd.isna(raw_coverage) or str(raw_coverage).strip().lower() in ["", "nan", "none"]

        is_valid_coverage = False
        if not is_empty_coverage:
            try:
                clean_coverage = str(raw_coverage).replace("$", "").replace("%", "").strip()
                
                if float(clean_coverage) >= 0:
                    is_valid_coverage = True
            except ValueError:
                print(f"DEBUG: Unreadable Coverage at row {index + 2}: '{raw_coverage}'")
                is_valid_coverage = False 
                

        constraints = {
            "START": isinstance(record.get("START"), str) and str(record.get("START")).strip() != "nan",
            "STOP": str(record.get("STOP", "")).strip() == "nan" or str(record.get("STOP", "")).strip() != "",
            "PATIENT": isinstance(record.get("PATIENT"), str) and str(record.get("PATIENT")).strip() != "nan",
            "PAYER": isinstance(record.get("PAYER"), str) and str(record.get("PAYER")).strip() != "nan",
            "ENCOUNTER": isinstance(record.get("ENCOUNTER"), str) and str(record.get("ENCOUNTER")).strip() != "nan",
            "CODE": str(record.get("CODE", "")).strip() != "" and str(record.get("CODE", "")).strip() != "nan",
            "DESCRIPTION": isinstance(record.get("DESCRIPTION"), str) and str(record.get("DESCRIPTION")).strip() != "nan",
            "BASE_COST": isinstance(record.get("BASE_COST"), (int, float)) and record.get("BASE_COST", -1) >= 0,
            
            "PAYER_COVERAGE": is_empty_coverage or is_valid_coverage,
            
            "DISPENSES": isinstance(record.get("DISPENSES"), (int, float)) and record.get("DISPENSES", -1) >= 0,
            "TOTALCOST": isinstance(record.get("TOTALCOST"), (int, float)) and record.get("TOTALCOST", -1) >= 0
        }
        
        failed_columns = [column for column, passed in constraints.items() if not passed]
        
        if failed_columns:
            bad_rows.append({
                "csv_row": index + 2,
                "patient": record.get("PATIENT", "Unknown"),
                "failed_rules": failed_columns
            })
            
    return bad_rows 


if __name__ == "__main__":
    records_data = validate(filename)
    
    if records_data:
        print("Success: Valid Format. Checking constraints...\n")
        
        bad_records = find_invalid_records(records_data)
        
        if not bad_records:
            print("All records have been validated successfully.")
        else:
            print(f"Found {len(bad_records)} invalid records.")
            
    else:
        print("Pipeline stopped because the file format was invalid.")
