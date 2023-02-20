import streamlit as st
from utils import _preprocess, log_result, show_history, load_json_lines

index_file = './index_file/gpt_index_docs.json'
log_file = './log/simple_app_log.txt'
max_tokens = 512


@st.cache(allow_output_mutation=True)
def preprocess():
    return _preprocess(index_file, max_tokens=max_tokens)


if __name__ == '__main__':
    index, llm_model = preprocess()

    q = st.text_input('query:')
    lang = st.selectbox('Language:', ['', 'Japanese', 'English'])
    send_q = st.button('send')
    # model_selected = st.selectbox('predictor model:', list(llm_model.keys()))
    # index._llm = llm_model[model_selected]

    if send_q:
        if lang:
            q += ' (in {})'.format(lang)
        res = index.query(q)
        st.markdown(res.response)
        log_result(res, {'Q': q}, log_file)

    logs = load_json_lines(log_file)
    show_history(logs, index)

