
import os
from dotenv import load_dotenv

load_dotenv()
import streamlit as st

# GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")
MODEL_NAME     = "gemini-1.5-flash"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

STUDENT_PARAMS_CSV = "Creating_Section_Params/data/langchain_student_params_1500_reduced.csv"
SECTION_PARAMS_CSV = "Creating_Section_Params/data/next_section_ranges_chatgpt.csv.csv"
OUTPUT_CSV = "Creating_Section_Params/output/ground_truth_sections_params_temp0.csv"
