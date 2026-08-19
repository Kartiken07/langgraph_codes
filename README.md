## Projects

### 1. LangGraph Basics (`1_langgraph_prompting.ipynb`)
- State graph with typed state (`BlogState`)
- Blog generation pipeline: title → outline → final blog
- Uses HuggingFace LLM endpoint

### 2. Tweet Generator & Optimizer (`3_gen_tweet_and_optmize_it.ipynb`)
- Generates tweets using LLM
- Optimizes content with AI feedback loop

### 3. LangGraph Chatbot (`4_langgrapg_chat_bot.ipynb`)
- Stateful chatbot using LangGraph
- Groq LLM (llama-3.1-8b-instant) with MemorySaver
- Message history management with `add_messages`

### 4. Chatbot with SQLite Persistence (`5_langgraph_presistance.ipynb`)
- Persistent chat history using SQLite checkpointing
- Thread-based conversation management
- `InMemorySaver` for session state

### 5. Streamlit Chatbot UI (`langgraph_chatbot/`)
- Full-stack chatbot with Streamlit frontend
- SQLite backend for conversation storage
- New chat creation and history loading

### 6. LangSmith Masterclass - RAG Pipeline (`RAG_chat_with_langsmith/langsmith-masterclass/`)
- `1_simple_llm_call.py` - Basic LLM call with LCEL chain
- `2_sequential_chain.py` - Sequential chain execution
- `3_rag_v1.py` to `3_rag_v4.py` - Iterative RAG implementations using FAISS + PDF (ISLR textbook)
- `4_agent.py` - ReAct agent with DuckDuckGo search + weather API tools

## Tech Stack
- **Frameworks:** LangGraph, LangChain, LangSmith
- **LLMs:** Groq (llama-3.1-8b-instant, allam-2-7b, gpt-oss-20b), HuggingFace
- **Vector Store:** FAISS
- **Embeddings:** sentence-transformers/all-MiniLM-L6-v2
- **Frontend:** Streamlit
- **DB:** SQLite (via LangGraph checkpointer)

## Setup

```bash
pip install langgraph langchain langchain-groq langchain-huggingface faiss-cpu streamlit python-dotenv
Create a .env file:
GROQ_API_KEY=your_groq_api_key
LANGCHAIN_API_KEY=your_langsmith_api_key
Run
# Streamlit chatbot
streamlit run langgraph_chatbot/langgraph_chatbot_with_sqllite_ui.py

# Individual scripts
python RAG_chat_with_langsmith/langsmith-masterclass/3_rag_v1.py
Author
Kartiken07
