import streamlit
# from auth.session_state import get as get_session
from auth.user import check_user


def login_component(st: streamlit):

    user_el = st.sidebar.empty()
    password_el = st.sidebar.empty()
    login_el = st.sidebar.empty()

    # session_info = get_session(user='', login=False)
    if_login = st.session_state.get('login')
    user = st.session_state.get('user')
    if if_login:
        st.sidebar.title('hello {}'.format(user))
        return True
    else:
        user = user_el.text_input('user_name')
        password = password_el.text_input('password', type='password')
        login = login_el.button('login')

        if login:
            if user and password:
                user_auth = check_user(user, password)
                if user_auth:
                    st.session_state.login = True
                    st.session_state.user = user
                    user_el.empty()
                    password_el.empty()
                    login_el.empty()
                    st.sidebar.title('hello {}'.format(user))
                    return True
    return False
