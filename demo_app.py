from auth.login import login_component
import streamlit as st
from utils import log_result, show_history

from utils import load_json, save_json, _preprocess, load_json_lines

index_file = './index_file/the_merge.json'
log_file = './log/demo_log.txt'
max_tokens = 512


def user_credit_path(user):
    return './config/credit_{}.json'.format(user)


def load_credit(user):
    path = user_credit_path(user)
    d = load_json(path)
    return d['credit']


def reset_credit(user, credit):
    path = user_credit_path(user)
    save_json(path, {'credit': credit})


@st.cache(allow_output_mutation=True)
def preprocess():
    return _preprocess(index_file, max_tokens)


if __name__ == '__main__':
    index, llm_model = preprocess()

    if_login = login_component(st)
    if if_login:
        user = st.session_state.get('user')
        credit = load_credit(user)

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

            log_result(res, {'Q': q, 'user': user}, log_file)
            credit -= 1
            reset_credit(user, credit)

        st.sidebar.write('hello {}, you have credit {}'.format(user, credit))

        logs = load_json_lines(log_file)
        logs = [l for l in logs if l.get('user') == user]
        show_history(logs, index)
