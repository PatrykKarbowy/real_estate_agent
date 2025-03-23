import streamlit as st
import requests

st.title("Znajdź swoją nieruchomość z AI!")
user_input = st.text_input("Wpisz to, jakiej nieruchomości szukasz (np. Mieszkanie w Krakowie do 150m2, cena maksymalna 150000zł):")

if st.button("Search"):
    response = requests.get("http://localhost:8000/search", params={"query": user_input})
    data = response.json()
    st.write("Filters:", data["filters"])

    st.subheader("Listings from OLX, Otodom, and Gratka")
    for listing in data["results"]:
        st.write(f"[{listing['title']}]({listing['url']}) - {listing['price']}")

    # Chat-like interaction
    st.subheader("Chat with AI")
    chat_input = st.text_input("Ask the AI about the listings (e.g., 'Show results in a table'):")
    if st.button("Send"):
        chat_response = requests.get("http://localhost:8000/chat",
                                     params={"query": chat_input, "listings": data["results"]})
        chat_data = chat_response.json()
        if chat_data.get("table_format"):
            st.table(chat_data["table_format"])
        else:
            st.write(chat_data["response"])