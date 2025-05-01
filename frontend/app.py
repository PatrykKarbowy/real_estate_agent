import streamlit as st
import requests

st.title("Znajdź swoją nieruchomość z AI!")

if "dom_content" not in st.session_state:
    st.session_state.dom_content = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

city_input = st.text_input("Wpisz miasto, w którym chcesz znaleźć nieruchomości")

if st.button("Szukaj"):
    if city_input:
        st.write("Wyszukiwanie nieruchomości...")

        response = requests.get("http://localhost:8000/search", params={"city": city_input})
        if response.status_code == 200:
            data = response.json()
            st.session_state.dom_content = data.get("listings", [])
            st.session_state.chat_history = []
        else:
            st.error("Błąd podczas pobierania ofert. Sprawdź połączenie z serwerem.")

if st.session_state.dom_content:
    st.subheader("Odczytane dane ze strony:")
    with st.expander("Zobacz oferty"):
        st.write(st.session_state.dom_content)

if st.session_state.dom_content:
    st.subheader("Porozmawiaj z czatem na temat tych danych!")

    for message in st.session_state.chat_history:
        role = "Ty" if message["role"] == "user" else "AI"
        st.write(f"**{role}:** {message['content']}")

    chat_input = st.text_input("Napisz przykładowo: ('Największe mieszkanie z podanych to?')")

    if st.button("Zapytaj") and chat_input:
        st.session_state.chat_history.append({"role": "user", "content": chat_input})

        chat_payload = {
            "query": chat_input,
            "listings": st.session_state.dom_content,
            "history": st.session_state.chat_history
        }

        chat_response = requests.post("http://localhost:8000/chat", json=chat_payload)

        if chat_response.status_code == 200:
            chat_data = chat_response.json()
            assistant_response = chat_data.get("response", "Brak odpowiedzi")
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
            st.write(f"**AI:** {assistant_response}")
        else:
            st.error("Błąd podczas komunikacji z serwerem czatu.")
