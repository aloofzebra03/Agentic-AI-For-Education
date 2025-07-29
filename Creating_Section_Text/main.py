# main.py
import argparse, json,sys

PROJECT_ROOT = r"C:/Users/aryan/Desktop/Personalized_Education/Personalized_Education"
sys.path.insert(0, PROJECT_ROOT)

from Creating_Section_Text.schema       import NextSectionChoice
from Creating_Section_Text.pipeline     import run_one, ingest_and_build_store

def main():
    p = argparse.ArgumentParser("RAG Next-Section")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("ingest", help="Load PDF & build vector store")

    gen = sub.add_parser("generate", help="Generate next section")
    gen.add_argument("--ongoing_concept",   required=True)
    gen.add_argument("--section_params_file", required=True,
                     help="JSON file matching NextSectionChoice schema")

    args = p.parse_args()

    if args.cmd == "ingest":
        print("Ingesting PDF and building vector store...")
        ingest_and_build_store()

    elif args.cmd == "generate":
        with open(args.section_params_file) as f:
            params = NextSectionChoice(**json.load(f))
        text = run_one(args.ongoing_concept, params)
        print(text)

    else:
        p.print_help()

if __name__ == "__main__":
    main()
