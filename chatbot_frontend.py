import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

# **************************************** Utility Functions *************************

def generate_thread_id():
    return str(uuid.uuid4())

def add_thread(thread_id, title="New Chat"):
    if not any(t['id'] == thread_id for t in st.session_state['chat_threads']):
        st.session_state['chat_threads'].append({'id': thread_id, 'title': title})

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    st.session_state['message_history'] = []
    add_thread(thread_id, title="New Chat")

def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']

# **************************************** Session Setup ******************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

# Ensure current thread is registered
add_thread(st.session_state['thread_id'])

# **************************************** Sidebar UI *********************************

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

# Unique key added here to avoid duplicate element error
for thread in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(thread['title'], key=f"thread_button_{thread['id']}"):
        st.session_state['thread_id'] = thread['id']
        messages = load_conversation(thread['id'])

        temp_messages = []
        for msg in messages:
            role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages

# **************************************** Main UI ************************************

# Editable chat title input
current_thread = next((t for t in st.session_state['chat_threads'] if t['id'] == st.session_state['thread_id']), None)
if current_thread:
    new_title = st.text_input("Chat Title", value=current_thread['title'], key="chat_title_input")
    if new_title != current_thread['title']:
        current_thread['title'] = new_title

# Display conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# User input box
user_input = st.chat_input('Type here')

if user_input:
    # Append user message
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            chunk.content for chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )

    # Append assistant response
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
