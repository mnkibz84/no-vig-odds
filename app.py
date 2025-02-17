import streamlit as st
import math
from decimal import Decimal, getcontext

def get_no_vig_odds_multiway(odds, accuracy=3):
    """
    Beräknar no-vig (fair) odds baserat på inmatade odds.
    """
    getcontext().prec = accuracy + 4  # Öka precision för beräkningar
    if any(o <= 1 for o in odds):
        st.error("Alla odds måste vara större än 1.")
        return []

    c, target_overround, current_error = Decimal(1), Decimal(0), Decimal(1000)
    max_error = Decimal(10) ** (-accuracy) / 2
    iteration_limit = 100  # Begränsning för att undvika oändlig loop
    iteration_count = 0
    
    while current_error > max_error and iteration_count < iteration_limit:
        f = Decimal(-1 - target_overround)
        f_dash = Decimal(0)

        for o in odds:
            inv_o = Decimal(1) / Decimal(o)
            f += inv_o ** c
            f_dash += (inv_o ** c) * (-inv_o.ln())  # ln = naturliga logaritmen
        
        if abs(f_dash) < Decimal('1E-10'):
            st.warning("Numerisk instabilitet upptäckt, använder justerad fallback-metod.")
            avg_prob = sum(1/o for o in odds)
            fair_odds = [round((1 / (1/o / avg_prob)), accuracy) for o in odds]
            return fair_odds
        
        h = -f / f_dash
        c += h
        
        t = sum((Decimal(1) / Decimal(o)) ** c for o in odds)
        current_error = abs(t - Decimal(1) - target_overround)
        iteration_count += 1
    
    fair_odds = [round(float(Decimal(o) ** c), accuracy) for o in odds]
    return fair_odds

# Streamlit UI
st.title("No-Vig Odds Kalkylator 🎲")
st.write("Ange odds för en marknad och få fair odds utan bookmaker-marginal.")

# Användarinput
odds_input = st.text_input("Ange odds separerade med komma (t.ex. 1.41, 4.2, 6.4, 22)")

if odds_input:
    try:
        odds = [float(o.strip()) for o in odds_input.split(",")]
        fair_odds = get_no_vig_odds_multiway(odds)
        if fair_odds:
            st.write("### Fair Odds")
            st.table({"Inmatade odds": odds, "Fair odds": fair_odds})
    except ValueError:
        st.error("Felaktig inmatning, vänligen använd endast nummer separerade med komma.")
