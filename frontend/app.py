import streamlit as st
import requests

st.title("Znajdź swoją nieruchomość z AI!")
city_input = st.text_input("Wpisz miasto, w którym chcesz znaleźć nieruchomości")

if st.button("Search"):
    response = requests.get("http://localhost:8000/search", params={"city": city_input})
    data = response.json()
    print(data)
    #st.write("City:", data["city"])

    # Chat-like interaction
    st.subheader("Chat with AI")
    chat_input = st.text_input("Ask the AI about the listings (e.g., 'Show results in a table'):")