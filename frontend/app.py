import streamlit as st
import requests

st.title("Znajdź swoją nieruchomość z AI!")

# Ensure session state variables exist
if "dom_content" not in st.session_state:
    st.session_state.dom_content = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Stores all messages exchanged with the LLM

city_input = st.text_input("Wpisz miasto, w którym chcesz znaleźć nieruchomości")

if st.button("Szukaj"):
    if city_input:
        st.write("Wyszukiwanie nieruchomości...")

        response = requests.get("http://localhost:8000/search", params={"city": city_input})
        if response.status_code == 200:
            data = response.json()

            # Store the fetched data in session state
            st.session_state.dom_content = data.get("listings", [])

            # Reset chat history when new listings are fetched
            st.session_state.chat_history = []
        else:
            st.error("Błąd podczas pobierania ofert. Sprawdź połączenie z serwerem.")

# Show listings if they exist
if st.session_state.dom_content:
    st.subheader("Odczytane dane ze strony:")
    with st.expander("Zobacz oferty"):
        st.write(st.session_state.dom_content)

# Chat-like interaction (enabled only if we have listings)
if st.session_state.dom_content:
    st.subheader("Porozmawiaj z czatem na temat tych danych!")

    # Display previous chat messages
    for message in st.session_state.chat_history:
        role = "Ty" if message["role"] == "user" else "AI"
        st.write(f"**{role}:** {message['content']}")

    chat_input = st.text_input("Napisz przykładowo: ('Największe mieszkanie z podanych to?')")

    if st.button("Zapytaj") and chat_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": chat_input})

        chat_payload = {
            "query": chat_input,
            "listings": st.session_state.dom_content,
            "history": st.session_state.chat_history  # Send full chat history
        }

        chat_response = requests.post("http://localhost:8000/chat", json=chat_payload)

        if chat_response.status_code == 200:
            chat_data = chat_response.json()
            assistant_response = chat_data.get("response", "Brak odpowiedzi")

            # Add AI response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

            # Display AI response
            st.write(f"**AI:** {assistant_response}")
        else:
            st.error("Błąd podczas komunikacji z serwerem czatu.")
