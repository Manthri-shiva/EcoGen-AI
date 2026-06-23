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

    /* Chat container */
    .chat-wrapper { width: 100%; }
    .chat-box { background: #071022; border-radius: 12px; padding: 18px; max-height: 65vh; overflow:auto; border: 1px solid #172033; }
    .message { margin: 8px 0; display:flex; max-width: 90%; }
    .message.user { margin-left: auto; justify-content:flex-end; }
    .bubble { padding: 12px 14px; border-radius: 12px; line-height:1.3; }
    .bubble.user { background: linear-gradient(90deg,#0f172a,#10243a); color:#e6eef8; border-radius:12px 12px 6px 12px; }
    .bubble.assistant { background: linear-gradient(180deg,#052033,#07283a); color:#dbeafe; border-radius:12px 12px 12px 6px; border:1px solid rgba(255,255,255,0.02); }
    .meta { font-size:0.8rem; color:#9fb4d8; margin-top:6px; }

    /* Source card */
    .source-card { background:#061a26; border:1px solid #123041; padding:8px; border-radius:8px; margin-top:8px; }
    .source-title { font-weight:600; color:#cfe8ff; }
    .source-name { color:#a9d1ff; font-size:0.9rem; }

    /* Mobile responsiveness */
    @media (max-width:600px){
        .chat-box { max-height: 55vh; padding:12px; }
        .bubble { font-size: 0.95rem; }
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
            "sources": [],
            "confidence": None,
        }
    ]

# Render chat history inside a scrollable container
def render_chat_history(messages):
    html_parts = ["<div class='chat-wrapper'><div class='chat-box'>"]
    for msg in messages:
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
        sources = msg.get("sources", []) or []
        confidence = msg.get("confidence")

        if role == "user":
            html_parts.append(f"<div class='message user'><div class='bubble user'>{content}</div></div>")
        else:
            # Assistant bubble with sources and confidence
            assistant_html = f"<div class='message'><div class='bubble assistant'>{content}"
            if confidence is not None:
                assistant_html += f"<div class='meta'>Confidence: {confidence:.2f}</div>"
            # Append sources as cards
            if sources:
                assistant_html += "<div style='margin-top:8px;'>"
                for src in sources:
                    # Show retrieved document names
                    assistant_html += f"<div class='source-card'><div class='source-title'>Source</div><div class='source-name'>{src}</div></div>"
                assistant_html += "</div>"

            assistant_html += "</div></div>"
            html_parts.append(assistant_html)

    html_parts.append("</div></div>")
    st.markdown("""%s""" % "".join(html_parts), unsafe_allow_html=True)

render_chat_history(st.session_state.rag_messages)

prompt = st.chat_input("Ask a sustainability question...")
if prompt:
    # Append user message and re-render
    st.session_state.rag_messages.append({"role": "user", "content": prompt})
    render_chat_history(st.session_state.rag_messages)

    # Show user bubble immediately
    try:
        with st.spinner("Generating answer..."):
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

        render_chat_history(st.session_state.rag_messages)
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
        render_chat_history(st.session_state.rag_messages)

