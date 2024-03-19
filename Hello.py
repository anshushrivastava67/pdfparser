import streamlit as st
from streamlit.logger import get_logger
import spacy

try:
    spacy.cli.download("en_core_web_md")
    print("Language model downloaded successfully.")
except Exception as e:
    print(f"Error downloading language model: {e}")

nlp = spacy.load('en_core_web_md')
LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="PDF Parser using spacy",
        page_icon="👋",
    )

    st.write("# PDF Parser 👋")

    st.sidebar.success("Select a demo above.")

    name = '<h2>Resume Matching</h2>'
    st.markdown(name, unsafe_allow_html=True)

    job_description_file = st.file_uploader("Upload Job Description PDF", type=["pdf"])
    resume_files = st.file_uploader("Upload Resume PDFs", type=["pdf"], accept_multiple_files=True)

    if job_description_file and resume_files:
        job_description_text = job_description_file.read().decode('utf-8')
        doc1 = nlp(job_description_text)

        similarities = {}
        for resume_file in resume_files:
            resume_text = resume_file.read().decode('utf-8')
            doc2 = nlp(resume_text)
            similarity = doc1.similarity(doc2)
            similarities[resume_file.name] = similarity

            html = f'<html><head><style>.match-score{{font-size:24px;font-weight:bold;color:#488f31;}}.content{{padding:20px;}}</style></head><div class="content"><div><h4><b>Resume:</b> {resume_file.name}</h4></div><p>{resume_text[:500]}...</p><div class="match-score">Match Score: {int(similarity*100)}%</div></div></html>'
            st.markdown(html, unsafe_allow_html=True)

        sorted_sim = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

        rows = ""
        for file_path, score in sorted_sim:
            rows += f"<tr><td>{file_path}</td><td>{score*100:.2f}%</td></tr>"

        table_html = '<h2>Ranking Table</h2><table><tr><th>Resume</th><th>Match %</th></tr>' + rows + '</table>'
        st.markdown(table_html, unsafe_allow_html=True)

if __name__ == "__main__":
    run()
