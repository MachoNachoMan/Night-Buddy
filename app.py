# ... (keep the top part: imports, title, messages setup, sidebar, chat display)

# User input
if prompt := st.chat_input("Whisper something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Hugging Face API call (free, uncensored model)
    import requests
    API_URL = f"https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"  # Swap to uncensored: e.g., "TheBloke/MythoMax-L2-13B-GGUF" for NSFW
    headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}
    
    # Build prompt with memory
    full_prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
    
    payload = {"inputs": full_prompt, "parameters": {"max_new_tokens": 200, "temperature": 0.7}}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        reply = response.json()[0]["generated_text"].split(full_prompt)[-1].strip()  # Extract new response
    else:
        reply = "Waves crash as I lean in, your words igniting the night—tell me more?"  # Fallback
    
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})