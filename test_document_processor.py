from modules.document_processor import extract_text

file_path = input("Enter your document path: ")

try:
    extracted_text = extract_text(file_path)

    print("\nDOCUMENT EXTRACTION SUCCESSFUL")
    print("=" * 50)
    print(extracted_text[:2000])

except Exception as error:
    print("Error:", error)