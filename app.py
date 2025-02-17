import streamlit as st
from oddsmath import get_no_vig_odds_multiway  # Importera funktionen från oddsmath.py

st.title("No-Vig Odds Kalkylator 🎲")
st.write("Ange odds för en marknad och få fair odds utan bookmaker-marginal.")

# Användarinput
odds_input = st.text_input("Ange odds separerade med komma (t.ex. 1.41, 4.2, 6.4, 22)")
accuracy = st.slider("Välj decimalprecision", 1, 6, 3)

if odds_input:
    try:
        odds = [float(o.strip()) for o in odds_input.split(",")]
        fair_odds = get_no_vig_odds_multiway(odds, accuracy)
        if fair_odds:
            st.success(f"Fair odds: {fair_odds}")
    except ValueError:
        st.error("Felaktig inmatning, vänligen använd endast nummer separerade med komma.")
