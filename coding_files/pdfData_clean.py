import pdfplumber

pdf_path = "data_work/odyssey.pdf"
raw_text_path = "data_work/odyssey_raw.txt"
clean_text_path = "data_work/odyssey_clean.txt"


pdf = pdfplumber.open(pdf_path)

raw_text = ""

for page in pdf.pages:
    page_text = page.extract_text()
    if page_text:
        raw_text = raw_text + page_text + "\n"

pdf.close()

raw_file = open(raw_text_path, "w", encoding="utf-8")
raw_file.write(raw_text)
raw_file.close()

print("PDF converted to raw text")


raw_file = open(raw_text_path, "r", encoding="utf-8")
text = raw_file.read()
raw_file.close()

lines = text.split("\n")
clean_lines = []

for line in lines:  
    line = line.strip()


    if len(line) < 5:
        continue

    
    if line.isdigit():
        continue

    
    if "Project Gutenberg" in line:
        continue
    if "www.gutenberg.org" in line:
        continue

    if line.isupper() and not line.startswith("BOOK"):
        continue


    clean_lines.append(line)

clean_text = ""

for line in clean_lines:
    clean_text = clean_text + line + "\n\n"

clean_file = open(clean_text_path, "w", encoding="utf-8")
clean_file.write(clean_text)
clean_file.close()

print("Raw text cleaned and saved")

