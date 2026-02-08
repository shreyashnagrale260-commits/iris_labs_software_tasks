import json
import numpy as np
from sentence_transformers import SentenceTransformer


file = open("data_work/odyssey_chunks.json", "r", encoding="utf-8")
chunks = json.load(file)
file.close()

print("Total chunks loaded:", len(chunks))

model = SentenceTransformer("all-MiniLM-L6-v2")


embeddings = []
metadata = []   

for chunk in chunks:
    text = chunk["text"]


    vector = model.encode(text)
    vector = vector / np.linalg.norm(vector)
    embeddings.append(vector)


    metadata.append({
        "id": chunk["id"],
        "text": chunk["text"],
        "chapter": chunk["chapter"],
        "para_range": chunk["para_range"],
        "source": chunk["source"]
    })

print("Embeddings created")

embeddings_array = np.array(embeddings)

np.save("data_work/embeddings.npy", embeddings_array)

meta_file = open("data_work/metadata.json", "w", encoding="utf-8")
json.dump(metadata, meta_file, indent=2)
meta_file.close()

print("Embeddings saved to data_work/embeddings.npy")
print("Metadata saved to data_work/metadata.json")
