import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main {
        background:rgb(243, 244, 246);
        color: #ffffff;
        padding: 2rem;
    }
    .sidebar .sidebar-content {
        background:rgb(243, 243, 244);
        padding: 1.5rem;
        border-radius: 10px;
    }
    .stTextInput textarea {
        background:rgb(255, 255, 255) !important;
        color: white !important;
        border-radius: 8px;
    }
    .stChatMessage {
        background:rgb(251, 251, 251);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #38bdf8;
        border-bottom: 2px solid #38bdf8;
        padding-bottom: 0.5rem;
    }
    .stSpinner > div {
        border-color: #38bdf8 transparent transparent transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.title("🏗️ AI Solution Architect")
st.caption("Transform requirements into technical blueprints with DeepSeek R1")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Settings")
    model_choice = st.selectbox(
        "Select Model Version",
        ["deepseek-r1:1.5b", "deepseek-r1:3b"],
        index=0
    )
    st.divider()
    st.markdown("**Capabilities:**")
    st.markdown("- System Architecture Design")
    st.markdown("- Technology Stack Recommendations")
    st.markdown("- Workflow Diagrams (ASCII)")
    st.markdown("- Scalability Planning")
    st.divider()
    st.markdown("💡 **Pro Tip:** Be specific about requirements for best results")

# Initialize LLM Engine
try:
    llm = ChatOllama(
        model=model_choice,
        base_url="http://localhost:11434",
        temperature=0.25
    )
except Exception as e:
    st.error(f"❌ Model Error: {str(e)}")
    st.stop()

# System Prompt Configuration
system_prompt = SystemMessagePromptTemplate.from_template(
    """You are a 🏗️ **Senior Solution Architect**. Break down complex problems into:
1.  **Architectural components 🏛️**
2.  **Technology stack recommendations 🛠️**
3.  **Data flow diagrams (ASCII) 🔄**
4.  **Key implementation steps 📌**
5.  **Potential challenges ⚠️**
6.  **Scalability considerations 📈**

Format responses using **Markdown** with clear section headers."""
)

# Chat History Management
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "ai", "content": "🔍 Describe your technical challenge or requirement..."}
    ]

# Display Chat History
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input Handling
user_input = st.chat_input("Describe your problem or requirement...")

def generate_design(query):
    prompt = ChatPromptTemplate.from_messages([
        system_prompt,
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"input": query})

if user_input:
    # Add user message to history
    st.session_state.history.append({"role": "user", "content": user_input})
    
    # Generate and display response
    with st.chat_message("ai"):
        with st.spinner("🧠 Architecting solution..."):
            try:
                response = generate_design(user_input)
                st.markdown(response)
                st.session_state.history.append({"role": "ai", "content": response})
            except Exception as e:
                st.error(f"🚨 Generation Error: {str(e)}")