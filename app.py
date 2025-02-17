import streamlit as st
import math
from decimal import Decimal, getcontext

def get_no_vig_odds_multiway(odds, accuracy=3):
    """
    Beräknar no-vig (fair) odds baserat på inmatade odds.
    """
    getcontext().prec = accuracy + 2  # Sätt precision
    if any(o <= 1 for o in odds):
        st.error("Alla odds måste vara större än 1.")
        return []

    c, target_overround, current_error = Decimal(1), Decimal(0), Decimal(1000)
    max_error = Decimal(10) ** (-accuracy) / 2
    
    while current_error > max_error:
        f = Decimal(-1 - target_overround)
        f_dash = Decimal(0)

        for o in odds:
            inv_o = Decimal(1) / Decimal(o)
            f += inv_o ** c
            f_dash += (inv_o ** c) * (-inv_o.ln())  # ln = naturliga logaritmen
        
        h = -f / f_dash
        c += h
        
        t = sum((Decimal(1) / Decimal(o)) ** c for o in odds)
        current_error = abs(t - Decimal(1) - target_overround)
    
    fair_odds = [round(float(Decimal(o) ** c), accuracy) for o in odds]
    return fair_odds

# Streamlit UI
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
