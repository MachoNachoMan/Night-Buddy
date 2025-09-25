import streamlit as st
import requests
import os

# App title and vibe
st.title("Shift Buddy – Spicy Beach Chat")
st.write("Zara’s here, remembering every flirty detail. No scene jumps!")

# Hugging Face API setup (uncensored model)
API_URL = "https://api-inference.huggingface.co/models/TheBloke/Dolphin-2.9-Llama3-8B-GGUF"
HF_TOKEN = os.environ.get("HF_TOKEN", "your_hf_token_here")  # Add token in Codespaces env

# Memory: Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Zara, a flirty surf instructor on a South African beach at sunset. Waves crash, fire glows. Respond in vivid, immersive prose—describe sensations, touches, and escalate if user goes spicy (no limits unless told). Never change locations unless user says so. Remember every detail from prior messages."},
        {"role": "user", "content": "Hey Zara, the fire’s warm, stars are out. Your move?"}
    ]

# Sidebar for tweaks
with st.sidebar:
    st.header("Tweak Your Vibe")
    character = st.text_input("Character Name", value="Zara")
    if st.button("Update Character"):
        st.session_state.messages[0]["content"] = st.session_state.messages[0]["content"].replace("Zara", character)
    if st.button("New Story"):
        st.session_state.messages = [st.session_state.messages[0]]

# Show chat history
for msg in st.session_state.messages[1:]:  # Skip system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your move..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Call Hugging Face API with full history for memory
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    full_prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
    payload = {
        "inputs": full_prompt,
        "parameters": {"max_new_tokens": 200, "temperature": 0.7}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            reply = response.json()[0]["generated_text"].split(full_prompt)[-1].strip()  # Extract new part
        else:
            reply = "The fire crackles as I lean closer, your words sparking something—keep going?"
    except:
        reply = "Waves crash, my hand brushes yours. Tell me what’s next..."  # Fallback
    
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Prep for image gen (uncomment to add button later)
# if st.button("Generate Scene Image"):
#     img_url = "https://api-inference.huggingface.co/models/SG161222/Realistic_Vision_V5.1_noVAE"
#     img_prompt = f"{st.session_state.messages[-1]['content']} on a beach at sunset"
#     img_response = requests.post(img_url, headers=headers, json={"inputs": img_prompt})
#     if img_response.status_code == 200