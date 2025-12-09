import streamlit as st
from streamlit_option_menu import option_menu
import requests
import uuid

API_URL = st.secrets["API_URL"]


st.set_page_config(page_title="DocuChat.io", page_icon="💬", layout="centered")


# ---------------------------------------------------------
# SESSION STATE (PERSIST ACROSS RELOAD)
# ---------------------------------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = ""   # User will enter manually

if "upload_result" not in st.session_state:
    st.session_state.upload_result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------------------
# Sidebar Title
# ---------------------------
st.sidebar.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color:#61D640;">NAVIGATION</h1>
        <br><br> 
    """,
    unsafe_allow_html=True
)


# ------------------ Sidebar Styling ------------------
st.markdown(
    """
    <style>
        .stApp {
            background-color: #0d1117;
        }
        [data-testid="stSidebar"] {
            background-color: #0d1117;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------ Sidebar Menu ----------------------
with st.sidebar:
    page = option_menu(
        menu_title=None,
        options=["Home" , "Upload Document", "Chat"],
        icons=["house" , "chat-dots", "robot"],
        default_index=0,
        styles={
            "container": {
                "padding": "0 !important",
                "background-color": "#0d1117",
            },
            "icon": {
                "color": "white",
                "font-size": "20px",
            },
            "nav-link": {
                "color": "white",
                "font-size": "18px",
                "text-align": "left",
                "margin": "5px 0",
                "--hover-color": "#1a1f24",
            },
            "nav-link-selected": {
                "background-color": "#161b22",
                "border-radius": "10px",
                "color": "white",
                "font-weight": "600",
            },
        }
    )


# ---------------------------------------------------------
# Home Page
# ---------------------------------------------------------

if page == "Home":

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
        Intelligent Document Assistant — Ask anything about your PDFs instantly and get context and history aware answers
    </h4>
    <br><br>
    """,
    unsafe_allow_html=True,
    )

    # --- DEMO VIDEO BUTTON ---
    demo_url = "https://drive.google.com/file/d/1l3UTh-sXufC5-h8DUUvKQJMBzM_eLiaJ/view?usp=drive_link"

    

    if st.button("Check Demo Video"):
        st.markdown(f"[▶ Click to Play Demo Video]({demo_url})")



# ---------------------------------------------------------
# UPLOAD DOCUMENT PAGE
# ---------------------------------------------------------
elif page == "Upload Document":

    st.markdown(
        """
        <div style="
            padding: 20px;
            border-radius: 10px;
            background: linear-gradient(135deg, #5b86e5, #36d1dc);
            text-align: center;
            color: white;
        ">
            <h3>Upload Your Document</h3>
            <p>Supports PDF & DOCX</p>
        </div>
        <br>
        """,
        unsafe_allow_html=True
    )

    # Ask user for session_id
    st.session_state.session_id = st.text_input(
        "Enter Your User ID (Session ID):",
        placeholder= "e.g. user123",
        value=st.session_state.session_id
    )

    file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx"],
        help="Upload your document to start chatting",
    )

    if st.session_state.upload_result:
        st.success(
            f"📄 Document indexed into {st.session_state.upload_result['chunks']} chunks"
        )

    if file and st.button("📤 Upload & Index Document", use_container_width=True):

        if st.session_state.session_id.strip() == "":
            st.error("❌ Please enter a valid session ID")
        else:
            with st.spinner("🔄 Processing your document..."):

                files = {"file": (file.name, file, file.type)}

                response = requests.post(
                    f"{API_URL}/upload?session_id={st.session_state.session_id}",
                    files=files
                )

                if response.status_code == 200:
                    st.session_state.upload_result = response.json()
                    st.success("✅ Document successfully indexed!")

                else:
                    st.error(response.json().get("detail", "Upload failed"))


# ---------------------------------------------------------
# CHAT PAGE
# ---------------------------------------------------------
elif page == "Chat":

    st.markdown(
        """
        <h2 style='text-align:center; color:white;'>💬 Chat with Your Document</h2>
        <br>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.session_id:
        st.warning("⚠️ Enter your User ID in the Upload section first.")
        st.stop()

    if not st.session_state.upload_result:
        st.warning("⚠️ Upload a document first.")
        st.stop()

    # Show chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])
            if "sources" in msg:
                with st.expander("📎 Sources"):
                    for src in msg["sources"]:
                        st.write(f"• Page {src['page']:} — {src['meta']}")
                        st.write(src["content"])

    # Input box
    user_question = st.chat_input("Ask something about your document...")

    if user_question:
        st.chat_message("user").write(user_question)

        payload = {
            "session_id": st.session_state.session_id,
            "question": user_question
        }

        response = requests.post(f"{API_URL}/query", json=payload)

        if response.status_code == 200:
            data = response.json()
            answer = data["answer"]

            # Save user + assistant message
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer,
                "sources": data.get("sources", [])
            })

            st.chat_message("assistant").write(answer)

            # Show sources
            with st.expander("📎 Sources"):
                for src in data.get("sources", []):
                    st.write(f"• Page {src['page']} — {src['meta']}")
                    st.write(src["content"])

        else:
            st.error(response.json().get("detail", "Error"))



