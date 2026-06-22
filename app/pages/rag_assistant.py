import streamlit as st

from rag.chatbot.rag_assistant import ask_question


st.set_page_config(
    page_title="EcoGen AI RAG Assistant",
    page_icon="📘",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp { background: #0f172a; }
    .block-container { padding-top: 1rem; }
    div[data-testid="stChatMessage"] {
        background: #0b1220;
        border: 1px solid #1e293b;
        border-radius: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("📘 Sustainability Knowledge Assistant")
st.caption(
    "Ask questions about sustainability, climate guidance, renewable energy, and SDG-related topics."
)

if "rag_messages" not in st.session_state:
    st.session_state.rag_messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I can help answer sustainability questions using the project's knowledge base. "
                "Ask me about solar energy, climate topics, or SDG-related guidance."
            ),
        }
    ]

for message in st.session_state.rag_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message.get("role") == "assistant" and message.get("sources"):
            with st.expander("View retrieved sources"):
                for source in message["sources"]:
                    st.write(f"• {source}")

        if message.get("role") == "assistant" and message.get("confidence") is not None:
            st.caption(f"Confidence: {message['confidence']:.2f}")

prompt = st.chat_input("Ask a sustainability question...")
if prompt:
    st.session_state.rag_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        response = ask_question(prompt)
        answer = response.get("answer", "No answer was generated.")
        confidence = response.get("confidence", 0.0)
        sources = response.get("sources", [])

        st.session_state.rag_messages.append(
            {
                "role": "assistant",
                "content": answer,
                "confidence": confidence,
                "sources": sources,
            }
        )

        with st.chat_message("assistant"):
            st.write(answer)
            with st.expander("View retrieved sources"):
                if sources:
                    for source in sources:
                        st.write(f"• {source}")
                else:
                    st.write("No source citations were retrieved.")
            st.caption(f"Confidence: {confidence:.2f}")
    except Exception as exc:
        error_message = f"I couldn't answer that question right now. Error: {exc}"
        st.session_state.rag_messages.append(
            {
                "role": "assistant",
                "content": error_message,
                "confidence": 0.0,
                "sources": [],
            }
        )
        with st.chat_message("assistant"):
            st.write(error_message)

