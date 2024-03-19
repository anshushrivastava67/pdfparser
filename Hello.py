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

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="PDF Parser using spacy",
        page_icon="👋",
    )

    st.write("# PDF Parser 👋")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        <html><head><style>.match-score{font-size:24px;font-weight:bold;color:#488f31;}.content{padding:20px;}</style></head><div class="content"><div><h4><b>Resume:</b>' + file_name + '</h4></div><p>' + a[:500] + '...</p><div class="match-score">Match Score: ' + str(int(similarity*100)) + '%</div></div></html>
    """
    )


if __name__ == "__main__":
    run()
