import streamlit as st

pages = {
    "About": [
        st.Page("about/about_1.py", title="About", icon="📚")
    ],
    "Lexer": [
        st.Page("lexer/lexer_1.py", title="Lexer", icon="🧑‍💻"),
    ],
    "Semantic": [
        st.Page("semantic/semantic_1.py", title="Semantic", icon="🧠"),
    ],
    "Syntax": [
        st.Page("syntax/syntax_1.py", title="Syntax", icon="📝"),
    ],
    "Compiler" : [
        st.Page("compiler/compiler_1.py", title="Compiler", icon="🚀"),
    ],
}

pg = st.navigation(pages)
pg.run()
