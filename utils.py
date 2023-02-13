import datetime
import json
import os
import streamlit as st

from gpt_index import LLMPredictor, GPTSimpleVectorIndex
from langchain import OpenAI
from gpt_index.response.schema import Response


def load_json_lines(path):
    with open(path, 'r') as f:
        t_lt = f.readlines()
        d_lt = []
        for t in t_lt:
            try:
                d_lt.append(json.loads(t))
            except:
                pass
    return d_lt


def load_json(path):
    with open(path, 'r') as f:
        d_ = json.load(f)
    return d_


def save_json(path, obj):
    with open(path, 'w') as f:
        json.dump(obj, f)


def get_auth(path=''):
    auth_path = './config/auth.json'
    if not path:
        path = auth_path
    return load_json(path)


def get_llm_model(max_tokens=None):
    openai_kwargs = {'temperature': 0}
    if max_tokens:
        openai_kwargs['max_tokens'] = max_tokens

    llm_predictor_high = LLMPredictor(OpenAI(model_name="text-davinci-003", **openai_kwargs))
    # llm_predictor_cheep = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-ada-001"))
    # llm_predictor_cheep = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-babbage-001"))
    llm_predictor_cheep = LLMPredictor(llm=OpenAI(model_name="text-curie-001", **openai_kwargs))
    # llm_predictor_cheep = OpenAI(temperature=0, model_name="text-ada-001")
    model_map = {'high': llm_predictor_high, 'cheep': llm_predictor_cheep}
    return model_map


def _preprocess(index_file, max_tokens=None):
    os.environ['OPENAI_API_KEY'] = get_auth()['token']
    model_map = get_llm_model(max_tokens)
    index = GPTSimpleVectorIndex.load_from_disk(index_file, llm_predictor=model_map['high'])
    return index, model_map


def log_result(res: Response, info, log_file):
    with open(log_file, 'a') as f:
        n_str = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
        f.write('\n')
        log_obj = info
        log_obj['A'] = res.response
        log_obj['t'] = n_str
        log_obj['source'] = []
        for n in res.source_nodes:
            log_obj['source'].append({'doc_id': n.doc_id, 'node_info': n.node_info})
        json.dump(log_obj, f, ensure_ascii=False)


def show_history(logs, index: GPTSimpleVectorIndex):
    with st.expander('history'):
        st.write('')
        st.write('')
        st.write('')
        for l in logs[::-1]:
            st.write(l.get('t'))
            st.write('Q: {}'.format(l.get('Q')))
            st.write('A: {}'.format(l.get('A')))
            source = l.get('source')
            if source:
                try:
                    st.write('sources: ')
                    for s in source:
                        txt = index.docstore.get_document(s['doc_id']).text[s['node_info']['start']: s['node_info']['end']]
                        st.write(txt[:300])
                except:
                    pass
            st.write('--------------------')
