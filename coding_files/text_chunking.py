import json
import os


file = open("data_work/odyssey_clean.txt", "r", encoding="utf-8")
textdata = file.read()
file.close()


paragraphs = textdata.split("\n\n")
print("Total paragraphs exist:", len(paragraphs))


chunks_collection = []
current_chunk = ""
chunk_id = 0

current_book = "Unknown Chapter"
para_start = 0
global_para_count = 0   


for para in paragraphs:
    para = para.strip()

    if len(para) < 50:
        continue


    if para.upper().startswith("BOOK"):
        current_book = para
        continue

    
    if current_chunk == "":
        para_start = global_para_count + 1

    current_chunk = current_chunk + " " + para
    global_para_count = global_para_count + 1

    
    if len(current_chunk.split()) >= 300:
        chunk = {
            "id": chunk_id,
            "text": current_chunk.strip(),
            "chapter": current_book,
            "para_range": str(para_start) + "-" + str(global_para_count),
            "source": "The Odyssey - Project Gutenberg"
        }

        chunks_collection.append(chunk)

        chunk_id = chunk_id + 1
        current_chunk = ""


json_file = open("data_work/odyssey_chunks.json", "w", encoding="utf-8")
json.dump(chunks_collection, json_file, indent=2)
json_file.close()

print("Total chunks created:", len(chunks_collection))
print("Saved to data_work/odyssey_chunks.json")
