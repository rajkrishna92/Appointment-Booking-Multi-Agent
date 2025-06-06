import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/execute"

st.title("Appointment System")

# Session state to store conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

user_email = st.text_input("Enter your email:", "")
query = st.text_area("Enter your query:")

if st.button("Submit Query"):
    if user_email and query:
        try:
            # Append user message to conversation
            st.session_state.conversation.append({"role": "user", "content": query})

            response = requests.post(
                API_URL,
                json={
                    'messages': query,  # You can also send the full conversation if the backend supports it
                    'email': user_email
                },
                verify=False
            )
            
            if response.status_code == 200:
                ai_response = response.json()["output"]
                st.session_state.conversation.append({"role": "assistant", "content": ai_response})
                st.success("Response Received:")
            else:
                ai_response = f"Error {response.status_code}: Could not process the request."
                st.session_state.conversation.append({"role": "assistant", "content": ai_response})
                st.error(ai_response)
        except Exception as e:
            error_msg = f"Exception occurred: {e}"
            st.session_state.conversation.append({"role": "assistant", "content": error_msg})
            st.error(error_msg)
    else:
        st.warning("Please enter both email and query.")

# Display conversation history
st.subheader("Conversation History")
for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Assistant:** {msg['content']}")
