import streamlit as st
import requests

st.set_page_config(page_title="RealEstateAgent")
st.title("Znajdź swoją nieruchomość z AI!")

if "dom_content" not in st.session_state:
    st.session_state.dom_content = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.form("search_form", clear_on_submit=False):
    city_input = st.text_input("Wpisz miasto, w którym chcesz znaleźć nieruchomości")
    search_submitted = st.form_submit_button("Szukaj")

if search_submitted:
    if city_input.strip():
        st.info("Wyszukiwanie nieruchomości...")
        response = requests.get("http://localhost:8000/search", params={"city": city_input})
        if response.status_code == 200:
            data = response.json()
            st.session_state.dom_content = data.get("listings", [])
            st.session_state.chat_history = []
            st.success(f"Znaleziono {len(st.session_state.dom_content)} ofert.")
        else:
            st.error("Błąd podczas pobierania ofert. Sprawdź połączenie z serwerem.")
    else:
        st.warning("Podaj nazwę miasta.")

if st.session_state.dom_content:
    st.subheader("Odczytane dane ze strony:")
    with st.expander("Zobacz oferty"):
        st.write(st.session_state.dom_content)

if st.session_state.dom_content:
    st.subheader("Porozmawiaj z czatem na temat tych danych!")

    with st.form("chat_form", clear_on_submit=True):
        chat_input = st.text_input("Zadaj pytanie (np. 'Największe mieszkanie z podanych to?')", key="chat_input")
        chat_submitted = st.form_submit_button("Zapytaj")

    if chat_submitted and chat_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": chat_input})

        payload = {
            "query": chat_input,
            "listings": st.session_state.dom_content,
            "history": st.session_state.chat_history,
        }
        chat_resp = requests.post("http://localhost:8000/chat", json=payload)
        if chat_resp.status_code == 200:
            bot_msg = chat_resp.json().get("response", "Brak odpowiedzi")
            st.session_state.chat_history.append({"role": "assistant", "content": bot_msg})
        else:
            st.error("Błąd podczas komunikacji z serwerem czatu.")

    for idx, message in enumerate(st.session_state.chat_history):
        role = "Ty" if message["role"] == "user" else "AI"
        is_last = (idx == len(st.session_state.chat_history) - 1)
        with st.expander(f"{role}: {message['content'][:50]}...", expanded=is_last):
            st.markdown(f"**{role}:** {message['content']}")
