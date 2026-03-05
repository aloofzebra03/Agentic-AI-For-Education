import pandas as pd
import sys

PROJECT_ROOT = r"C:/Users/aryan/Desktop/Personalized_Education/Personalized_Education"
sys.path.insert(0, PROJECT_ROOT)

from Creating_Section_Params.config import STUDENT_PARAMS_CSV, OUTPUT_CSV
from Creating_Section_Params.schema import StudentParameters, NextSectionChoice
from Creating_Section_Params.prompt_builder import prompt, output_parser, SECTIONS
from Creating_Section_Params.model_loader import get_llm
import json

def process_row(row: dict) -> NextSectionChoice:
    #  Parse student and dump both current values and schema
    student_json = json.dumps(row, indent=2)
    student_schema_json = StudentParameters.model_json_schema()

    # Build and run chain
    llm = get_llm()
    llm_chain = prompt|llm|output_parser 
    raw = llm_chain.invoke({
        "student_json":student_json,
        "student_schema_json":student_schema_json,
        "sections":SECTIONS,
        # "next_section_parameter_ranges":next_section_parameter_ranges
         }
    )

    # 3. Parse & validate output
    print("Raw output:",raw)
    print("Output type:", type(raw))
    return raw

def main():
    # Read input profiles
    df = pd.read_csv(STUDENT_PARAMS_CSV)

    # Process each student
    records = []
    for _, row in df.iterrows():
        choice = process_row(row.to_dict())
        base   = row.to_dict()
        base.update({
            "next_section": choice.section_name,
            **choice.model_dump(exclude={"section_name"})
        })
        records.append(base)

    # Write ground truth CSV
    out_df = pd.DataFrame(records)
    out_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved ground truth to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
