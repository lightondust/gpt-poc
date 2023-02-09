import datetime
import os
import json
from gpt_index import GPTSimpleVectorIndex
from gpt_index import LLMPredictor
from langchain import OpenAI
import streamlit as st
from utils import load_json, save_json, _preprocess


index_file = './index_file/the_merge.json'
log_file = './log/simple_app_log.txt'


@st.cache(allow_output_mutation=True)
def preprocess():
    return _preprocess(index_file)


if __name__ == '__main__':
    index, llm_model = preprocess()

    q = st.text_input('query:')
    lang = st.selectbox('Language:', ['', 'Japanese', 'English'])
    send_q = st.button('send')
    model_selected = st.selectbox('predictor model:', list(llm_model.keys()))
    index._llm = llm_model[model_selected]

    if send_q:
        if lang:
            q += ' (in {})'.format(lang)
        res = index.query(q)
        st.markdown(res.response)
        with open(log_file, 'a') as f:
            n_str = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
            f.write('\n')
            json.dump({'Q': q, 'A': res.response, 't': n_str}, f, ensure_ascii=False)

