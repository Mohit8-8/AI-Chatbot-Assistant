import os
import streamlit as st
from openai import OpenAI


def init_session():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "api_key" not in st.session_state:
        st.session_state.api_key = get_default_api_key()


def get_default_api_key() -> str:
    return os.getenv("OPENAI_API_KEY", "")


def set_api_key(key: str):
    st.session_state.api_key = key


def get_client():
    if not st.session_state.api_key:
        return None
    return OpenAI(api_key=st.session_state.api_key)


def format_openai_error(error: Exception) -> str:
    error_text = str(error)
    if "insufficient_quota" in error_text or "exceeded your current quota" in error_text.lower():
        return (
            "Your OpenAI API quota is exhausted. "
            "Please check billing or add credits, then try again."
        )
    if "429" in error_text:
        return "OpenAI rate limit or quota reached. Please try again later or check billing."
    return f"OpenAI error: {error_text}"


def call_openai(messages):
    client = get_client()
    if client is None:
        return {"content": "", "error": "OpenAI API key not set."}
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=512,
            temperature=0.2,
        )
        return {"content": resp.choices[0].message.content or "", "error": ""}
    except Exception as e:
        return {"content": "", "error": format_openai_error(e)}


def main():
    st.set_page_config(page_title="AI Chatbot Assistant", layout="wide")
    init_session()

    st.title("AI Chatbot Assistant")

    with st.expander("API Key (recommended: set as env var OPENAI_API_KEY)"):
        api_input = st.text_input("OpenAI API key", type="password", value=st.session_state.api_key)
        if st.button("Set API Key"):
            set_api_key(api_input)
            st.success("API key set in session (not saved to disk).")

    if not st.session_state.api_key:
        st.warning("No API key set — set it above or export OPENAI_API_KEY in your environment.")

    col1, col2 = st.columns([3, 1])

    with col1:
        user_input = st.text_area("Message", height=120)
        if st.button("Send") and user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            messages = st.session_state.chat_history.copy()
            result = call_openai(messages)
            if result["error"]:
                st.error(result["error"])
                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": result["error"],
                    }
                )
            else:
                st.session_state.chat_history.append({"role": "assistant", "content": result["content"]})

    with col2:
        st.markdown("### Chat History")
        for msg in reversed(st.session_state.chat_history):
            prefix = "User" if msg["role"] == "user" else "Assistant"
            st.write(f"**{prefix}:** {msg['content']}")


if __name__ == "__main__":
    main()
