import os

import rootpath
import streamlit as st

from model import recommend_monster, monster_options, available_drinks
from modules.weather.api import get_weather
import requests

def get_user_location():
    try:
        res = requests.get("https://ipinfo.io/json")
        data = res.json()
        return data.get("city", "Amsterdam")  # fallback if unavailable
    except:
        return "Amsterdam"  # default fallback


# --- Streamlit UI ---
st.set_page_config(page_title="Monster Energy Oracle", page_icon="🧃")

st.title("⚡ Monster Energy Oracle")
st.subheader("Let the sky choose your caffeine.")

# Get list of all possible drinks
excluded = st.multiselect(
    "❌ Drinks to exclude from your destiny:",
    options=available_drinks,
    help="Don't like a flavor? Remove it from the prophecy."
)

if st.button("Tell me my drink of destiny"):
    city = get_user_location()
    print(city)
    weather = get_weather(city)
    rec = recommend_monster(weather, excluded)

    st.markdown(f"""
    ### 🧃 Your Monster:
    **{rec.drink_name}**""")

    title = rec.drink_name.lower().replace("monster", "").replace("energy", "").strip()
    print(title)
    if title in monster_options:
        image_path = os.path.join(rootpath.detect(), "drinks", "monster", monster_options[title])
        print(title)
        col1, col2 = st.columns([1,1])
        with col1:
            st.text(rec.explanation)

        with col2:
            if os.path.exists(image_path):
                st.image(image_path, width=500)
