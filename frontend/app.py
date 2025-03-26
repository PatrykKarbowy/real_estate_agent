import streamlit as st
import requests
import json

st.title("Znajdź swoją nieruchomość z AI!")

# Ensure session state variables exist
if "dom_content" not in st.session_state:
    st.session_state.dom_content = []

city_input = st.text_input("Wpisz miasto, w którym chcesz znaleźć nieruchomości")

if st.button("Szukaj"):
    if city_input:
        st.write("Wyszukiwanie nieruchomości...")

        response = requests.get("http://localhost:8000/search", params={"city": city_input})
        if response.status_code == 200:
            data = response.json()

            # Store the fetched data in session state to persist across reruns
            st.session_state.dom_content = data.get("listings", [])

        else:
            st.error("Błąd podczas pobierania ofert. Sprawdź połączenie z serwerem.")

# Show listings if they exist in session state
if st.session_state.dom_content:
    st.subheader("Odczytane dane ze strony:")
    with st.expander("Zobacz oferty"):
        st.write(st.session_state.dom_content)

# Chat-like interaction (Only enabled if we have listings)
if st.session_state.dom_content:
    st.subheader("Porozmawiaj z czatem na temat tych danych!")
    chat_input = st.text_input("Napisz przykładowo: ('Największe mieszkanie z podanych to?')")

    if st.button("Zapytaj") and chat_input:
        chat_payload = {"query": chat_input, "listings": st.session_state.dom_content}
        chat_response = requests.post("http://localhost:8000/chat", json=chat_payload)

        if chat_response.status_code == 200:
            chat_data = chat_response.json()
            st.write(chat_data.get("response", "Brak odpowiedzi"))
        else:
            st.error("Błąd podczas komunikacji z serwerem czatu.")

