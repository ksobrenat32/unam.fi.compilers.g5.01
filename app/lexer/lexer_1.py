import streamlit as st
from lexer.lexer import Lexer

st.header("Lexer")

source = st.text_area("Text to analyze")

if st.button("Tokenize"):
    lexer = Lexer(source)
    st.subheader("Tokens")

    # Format default dict
    tokenized = ""
    for key, value in lexer.tokenize().items():
        tokenized += f"{key}: {value}\n"
    st.success(tokenized)

    st.subheader("Token Count")
    st.success(lexer.token_count())
