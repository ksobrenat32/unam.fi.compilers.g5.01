import streamlit as st
from lexer.lexer import Lexer

# Set the page layout to wide
st.set_page_config(layout="wide")

st.header("Lexer")

# Create two columns
col1, col2 = st.columns(2)

with col1:
    source = st.text_area("Text to analyze", height=600)

with col2:
    if st.button("Tokenize"):
        lexer = Lexer(source)
        st.subheader("Tokens")

        # Format default dict
        tokenized = lexer.tokenize()
        for token_type, tokens in tokenized.items():
            st.markdown(f"**• <u>{token_type.capitalize()}</u>**", unsafe_allow_html=True)
            st.write(", ".join(tokens))

        st.subheader("Token Count")
        st.success(lexer.token_count())
