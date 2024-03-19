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

    def pdf_reader(file):
        resource_manager = PDFResourceManager()
        string_io = io.StringIO()
        converter = TextConverter(resource_manager, string_io, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        with open(file, 'rb') as fh:
            for page in PDFPage.get_pages(fh,
                                          caching=True,
                                          check_extractable=True):
                page_interpreter.process_page(page)
                print(page)
            text = string_io.getvalue()
    
        converter.close()
        string_io.close()
        return text


    import os
    
    name='<h2>Resume Matching</h2>'
    st.markdown(name, unsafe_allow_html=True)
    
    folder_path = r'C:\Users\anshu\Downloads\resume-20240212T152443Z-001\resume\Uploaded_Resumes'
    job_description=pdf_reader(r'C:\Users\anshu\Downloads\resume-20240212T152443Z-001\resume\job_description.pdf')
    similarities={}
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
     
            with open(file_path, 'r') as f:
                
                a=pdf_reader(file_path)
                doc1 = nlp(job_description)
                doc2 = nlp(a)
               
                similarity = doc1.similarity(doc2) 
                similarities[file_name]=similarity
    
                html = '<html><head><style>.match-score{font-size:24px;font-weight:bold;color:#488f31;}.content{padding:20px;}</style></head><div class="content"><div><h4><b>Resume:</b>' + file_name + '</h4></div><p>' + a[:500] + '...</p><div class="match-score">Match Score: ' + str(int(similarity*100)) + '%</div></div></html>'
                st.markdown(html, unsafe_allow_html=True)
    
    sorted_sim = []
    
    for k, v in similarities.items():
      sorted_sim.append((v, k)) 
       
    
    #here ia m doing bubble sort in descending order
    for i in range(len(sorted_sim)):
      for j in range(len(sorted_sim)-i-1):
       
        if sorted_sim[j][0] < sorted_sim[j + 1][0]:
          temp = sorted_sim[j]
          sorted_sim[j]= sorted_sim[j + 1]
          sorted_sim[j + 1]= temp
    
    rows = ""   
    for score, file_path in sorted_sim:
        rows += f"<tr><td>{file_path}</td><td>{score*100:.2f}%</td></tr>"
    
    table_html = '<h2>Ranking Table</h2><table><tr><th>Resume</th><th>Match %</th></tr>'+rows+'</table> '
    st.markdown(table_html, unsafe_allow_html=True)


if __name__ == "__main__":
    run()
