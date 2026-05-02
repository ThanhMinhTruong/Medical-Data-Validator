import pandas as pd

filename = "./bigmac.csv"

df = pd.read_csv(filename)
df = df[["START", "STOP", "PATIENT", "PAYER", "ENCOUNTER", "CODE", "DESCRIPTION", "BASE_COST", "PAYER_COVERAGE", "DISPENSES", "TOTALCOST", "REASONCODE", "REASONDESCRIPTION"]]
medical_records  = df.to_dict()

def validate(data):
    is_sequence = isinstance(data, (list, tuple))

    if not is_sequence:
        raise ValueError("Invalid Format: Expected a sequence (list or tuple) of medical records.")
    is_invalid = False
    
    for index,dictionary in enumerate(data):
        if not isinstance(disctionary,dict):
            raise ValueError(f"Invalid Format: Record at index {index} is not a dictionary.")
        is_invalid = True
        if is_invalid:
            return False
        print(f"Valid Format: Record at index {index} is a valid dictionary.")
        return True


if __name__ == "__main__":
    is_valid = validate(medical_records)
    