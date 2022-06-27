import requests
import streamlit as st


def header():
    """
    This function forms the header for the simple
    web frontend
    :return:
    """
    st.header("Welcome to URL shortener")
    st.subheader("Encode or Decode your URLs")


def url_encoder_form():
    """
    This function creates a form that takes a normal URL from
    the user and encodes it in a shortened form
    :return:
    """
    with st.form("url_encoder", clear_on_submit=False):
        url = st.text_input("URL that needs to be shortened")
        submit = st.form_submit_button("Shorten URL")
        if submit:
            res = requests.post(f"http://api:5000/encode?url={url}")
            if res.status_code == 200:
                st.text(res.json()["message"])
            else:
                st.text(f"There was an error: {res.json()['message']}")


def url_decoder_form():
    """
    This function creates a form that takes a shortened URL from
    the user and decodes it back to the actual URL.
    :return:
    """
    with st.form("url_decoder", clear_on_submit=False):
        url = st.text_input("URL that needs to be decoded")
        submit = st.form_submit_button("Decode URL")
        if submit:
            res = requests.get(f"http://api:5000/decode?url={url}")
            if res.status_code == 200:
                st.text(res.json()["message"])
            else:
                st.text(f"There was an error: {res.json()['message']}")


if __name__ == "__main__":
    header()
    url_encoder_form()
    url_decoder_form()
