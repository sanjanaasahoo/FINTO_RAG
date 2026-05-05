import streamlit as st
from rag_pipeline import rag_pipeline

st.set_page_config(
    page_title="FINTO - Financial RAG Chatbot",
    layout="centered"
)

# =====================
# PREMIUM CHARCOAL + GOLD THEME
# =====================
st.markdown("""
<style>
body {
    background-color: #1c1c24;
}

.main {
    background-color: #1c1c24;
}

h1 {
    color: #C9A227;
    text-align: center;
    font-weight: 700;
    letter-spacing: 1px;
}

label {
    color: #d1d1d1 !important;
    font-weight: 500;
}

/* Input */
.stTextInput > div > div > input {
    background-color: #2a2a36;
    color: #ffffff;
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #3a3a48;
}

/* Button */
.stButton > button {
    background-color: #C9A227;
    color: black;
    border-radius: 10px;
    padding: 10px 22px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background-color: #d4af37;
    color: black;
}

/* Answer card */
.answer-box {
    background-color: #2a2a36;
    padding: 20px;
    border-radius: 12px;
    border-left: 4px solid #C9A227;
    color: #eaeaea;
    margin-top: 20px;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# =====================
# UI
# =====================
st.markdown("<h1>💰 FINTO - Financial RAG Chatbot</h1>", unsafe_allow_html=True)

query = st.text_input("Ask your financial question:")

if st.button("Ask"):
    if query.strip() == "":
        st.warning("Please enter a question")
    else:
        try:
            with st.spinner("Generating answer..."):
                answer = rag_pipeline(query)

                st.markdown(
                    f"""
                    <div class="answer-box">
                        <b>Answer:</b><br><br>
                        {answer}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        except Exception as e:
            st.error(f"Error: {e}")