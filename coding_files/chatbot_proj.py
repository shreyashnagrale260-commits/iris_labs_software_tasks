import streamlit as st
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


@st.cache_resource
def load_resources():
    index = faiss.read_index("data_work/faiss.index")

    with open("data_work/metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    return index, metadata, model


index, metadata, model = load_resources()


st.title("Odyssey RAG Q&A Bot")
st.write("Answers are generated **only from retrieved passages** of *The Odyssey*.")

question = st.text_input("Ask a question:")


if question:
    
    q_vec = model.encode(question)
    q_vec = q_vec / np.linalg.norm(q_vec)
    q_vec = np.array([q_vec])

   
    k = 3
    distances, indices = index.search(q_vec, k)

    if len(indices[0]) == 0:
        st.error("This question is not relevant to the provided text")
    else:
        ans_sentences = []
        references = []

     
        for idx in indices[0]:
            chunk = metadata[idx]["text"]
            references.append(
                f"{metadata[idx]['chapter']} | Paragraphs {metadata[idx]['para_range']}"
            )

            sentences = chunk.split(".")
            for s in sentences:
                s = s.strip()
                if len(s) > 30:
                    ans_sentences.append(s)

        if len(ans_sentences) == 0:
            st.error("This question is not relevant to the provided text")
        else:
            
            sent_embeddings = model.encode(ans_sentences)

            similarities = np.dot(sent_embeddings, q_vec[0]) / (
                np.linalg.norm(sent_embeddings, axis=1) * np.linalg.norm(q_vec[0])
            )

            best_idx = int(np.argmax(similarities))
            best_score = similarities[best_idx]

           
            if best_score < 0.35:
                st.error("This question is not relevant to the provided text")
            else:
                answer = ans_sentences[best_idx]

            
                st.subheader("Answer")
                st.write(answer)

                st.subheader("References")

                seen = set()
                count = 0

                for ref in references:
                    if ref not in seen:
                        seen.add(ref)
                        st.write("- ", ref)
                        count += 1

                    if count == 2:
                        break
