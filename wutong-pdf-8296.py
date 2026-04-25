import argparse
import fitz  # PyMuPDF
from typing import List

def merge_pdfs(input_files: List[str], output_file: str) -> None:
    merger = fitz.open()
    for file in input_files:
        merger.insert_pdf(fitz.open(file))
    merger.save(output_file)
    print(f"PDFs merged successfully into {output_file}")

def split_pdf(input_file: str, output_folder: str) -> None:
    pdf_document = fitz.open(input_file)
    num_pages = len(pdf_document)
    for i in range(num_pages):
        page = pdf_document.load_page(i)
        output_path = f"{output_folder}/page_{i+1}.pdf"
        page.save(output_path)
    print(f"PDF split into {num_pages} pages successfully")

def extract_text(input_file: str, output_file: str) -> None:
    doc = fitz.open(input_file)
    text = ""
    for page in doc:
        text += page.get_text("text")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Text extracted successfully into {output_file}")

def main() -> None:
    parser = argparse.ArgumentParser(description="PDF Tools - Merge, Split, Extract Text")
    subparsers = parser.add_subparsers()

    # Subparser for merge
    merge_parser = subparsers.add_parser("merge", help="Merge PDFs")
    merge_parser.add_argument("input_files", nargs="+", type=str, help="Input PDF files")
    merge_parser.add_argument("--output", dest="output_file", required=True, help="Output PDF file")

    # Subparser for split
    split_parser = subparsers.add_parser("split", help="Split PDF into individual pages")
    split_parser.add_argument("input_file", type=str, help="Input PDF file")
    split_parser.add_argument("--output_folder", dest="output_folder", required=True, help="Output folder to save individual pages")

    # Subparser for extract text
    extract_text_parser = subparsers.add_parser("extract", help="Extract text from a PDF")
    extract_text_parser.add_argument("input_file", type=str, help="Input PDF file")
    extract_text_parser.add_argument("--output", dest="output_file", required=True, help="Output text file")

    args = parser.parse_args()

    if args.merge:
        merge_pdfs(args.input_files, args.output_file)
    elif args.split:
        split_pdf(args.input_file, args.output_folder)
    elif args.extract:
        extract_text(args.input_file, args.output_file)
    else:
        print("No subcommand specified")

if __name__ == "__main__":
    main()