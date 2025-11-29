import streamlit as st

st.set_page_config(
    page_title="Document Chatbot",
    page_icon="💬",
    layout="centered"
)


# --- PAGE TITLE ---
st.markdown(
    """
    <h1 style='text-align: center; color: #white;'>
        📚 DocuChat.io
    </h1>
    """,
    unsafe_allow_html=True,
)


# --- TAGLINE ---
st.markdown(
    """
    <br><br>
    <h4 style='text-align: center; font-weight: normal; color: #white;'>
        Intelligent Document Assistant — Ask anything about your PDFs instantly
    </h4>
    <br><br>
    """,
    unsafe_allow_html=True,
)


st.markdown(
        """
        <div style="
            background-color: #ffffff;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
            text-align: center;
        ">
            <h3 style="color: #444;">Upload your document</h3>
            <p style="color: #777;">PDF or DOCX supported</p>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)

file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx"],
        help="Upload your document to start chatting"
    )