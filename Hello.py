# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import spacy
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io
import re
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
        def preprocess_text(text):
            # Remove newlines and excess whitespace
            text = re.sub(r'\s+', ' ', text)
            return text
        
        def pdf_reader(file):
                
                resource_manager = PDFResourceManager()
                string_io = io.BytesIO()
                converter = TextConverter(resource_manager, string_io, laparams=LAParams())
                page_interpreter = PDFPageInterpreter(resource_manager, converter)
        
                for page in PDFPage.get_pages(io.BytesIO(file), caching=True, check_extractable=True):
                        page_interpreter.process_page(page)
        
                text = string_io.getvalue()
                converter.close()
                string_io.close()
                return text
                job_description_file = st.file_uploader("Upload Job Description PDF", type=["pdf"])
                resume_files = st.file_uploader("Upload Resume PDFs", type=["pdf"], accept_multiple_files=True)

                if job_description_file and resume_files:
                        job_description_bytes = job_description_file.read()
                        job_description_text = preprocess_text(pdf_reader(job_description_bytes))
                        doc1 = nlp(job_description_text)
        
                        similarities = {}
                        for resume_file in resume_files:
                            resume_bytes = resume_file.read()
                            resume_text = preprocess_text(pdf_reader(resume_bytes))
                            doc2 = nlp(resume_text)
                            similarity = doc1.similarity(doc2)
                            similarities[resume_file.name] = similarity

                sorted_sim = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

                rows = ""
                for file_path, score in sorted_sim:
                        rows += f"<tr><td>{file_path}</td><td>{score*100:.2f}%</td></tr>"

                table_html = '<h2>Ranking Table</h2><table><tr><th>Resume</th><th>Match %</th></tr>' + rows + '</table>'
                st.markdown(table_html, unsafe_allow_html=True)


if __name__ == "__main__":
    run()
