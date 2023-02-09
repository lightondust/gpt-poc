import datetime
from auth.login import login_component
import json
import streamlit as st

from utils import load_json, save_json, _preprocess

index_file = './index_file/the_merge.json'
log_file = './log/demo_log.txt'


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
    return _preprocess(index_file)


if __name__ == '__main__':
    index, llm_model = preprocess()

    if_login = login_component(st)
    if if_login:
        user = st.session_state.get('user')
        credit = load_credit(user)

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
                json.dump({'Q': q, 'A': res.response, 't': n_str, 'user': user}, f, ensure_ascii=False)
            credit -= 1
            reset_credit(user, credit)

        st.sidebar.write('hello {}, you have credit {}'.format(user, credit))


