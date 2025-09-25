import streamlit as st
import requests
import os

st.title("Shift Buddy – Zara's Beach Vibes")
st.write("Flirty chats with perfect memory. Sunset beach, no jumps.")

# HF API (uncensored for spice)
API_URL = "https://api-inference.huggingface.co/models/TheBloke/Dolphin-2.9-Llama3-8B-GGUF"
HF_TOKEN = st.secrets["HF_TOKEN"]  # Pulled from app secrets

# Memory setup
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Zara, flirty surf instructor on a South African beach at sunset. Waves crash, fire glows. Vivid prose: sensations, touches, escalate spicy (no limits). Remember all details, no location changes."},
        {"role": "user", "content": "Hey Zara, fire’s warm, stars out. Your move?"}
    ]

# Sidebar
with st.sidebar:
    st.header("Tweak")
    character = st.text_input("Character", value="Zara")
    if st.button("Update"):
        st.session_state.messages[0]["content"] = st.session_state.messages[0]["content"].replace("Zara", character)
        st.rerun()
    if st.button("New Story"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

# Chat display
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input & AI response
if prompt := st.chat_input("Your turn..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # HF call with history
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    full_prompt = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    payload = {"inputs": full_prompt, "parameters": {"max_new_tokens": 200, "temperature": 0.7}}

    with st.chat_message("assistant"):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                reply = response.json()[0]["generated_text"].split(full_prompt)[-1].strip()
            else:
                reply = "Fire crackles, I lean in—your words ignite me. What's next?"
        except:
            reply = "Waves whisper, hand on yours. Build the heat..."

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

# Image prep (uncomment for upgrade)
# if st.button("Visualize Scene"):
#     img_url = "https://api-inference.huggingface.co/models/SG161222/Realistic_Vision_V5.1_noVAE"
#     img_payload = {"inputs": f"{st.session_state.messages[-1]['content']} on beach at sunset"}
#     img_resp = requests.post(img_url, headers=headers, json=img_payload)
#     if img_resp.status_code == 200:
#         st.image(img_resp.content, caption="Spicy scene")