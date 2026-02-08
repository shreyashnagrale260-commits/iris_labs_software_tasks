import numpy as np
import faiss


embeddings = np.load("data_work/embeddings.npy")

print("Loaded embeddings:", embeddings.shape)


dimension = embeddings.shape[1] 
index = faiss.IndexFlatIP(dimension)#will accept only n dimension of vectors


index.add(embeddings) #adding all vectors row-wise

print("Total vectors in index:", index.ntotal)


faiss.write_index(index, "data_work/faiss.index")

print("FAISS index saved")
