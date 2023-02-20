# how to run

Create an openai account to use the API, get your token.
Make an `config/auth.json` file(example: `config/auth_example.json`)

install streamlit and gpt-index
- https://docs.streamlit.io/library/get-started/installation
- https://gpt-index.readthedocs.io/en/latest/getting_started/installation.html

run streamlit app
```
streamlit run simple_app.py
```

# use your own index

make an index and save it
- https://gpt-index.readthedocs.io/en/latest/getting_started/starter_example.html

change the index path to yours of `index_file` in `simple_app.py`.
