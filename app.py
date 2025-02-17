import streamlit as st
from decimal import Decimal, getcontext

def get_no_vig_odds_multiway(odds, accuracy=3):
    """
    Beräknar no-vig (fair) odds baserat på inmatade odds.
    """
    getcontext().prec = accuracy + 6  # Ökar precisionen för beräkningar
    if any(o <= 1 for o in odds):
        st.error("Alla odds måste vara större än 1.")
        return []

    c = Decimal(1)
    target_overround = Decimal(0)
    current_error = Decimal(1000)
    max_error = Decimal(10) ** (-accuracy) / 2
    iteration_limit = 100  # För att undvika oändliga loopar
    iteration_count = 0
    
    while current_error > max_error and iteration_count < iteration_limit:
        f = Decimal(-1 - target_overround)
        f_dash = Decimal(0)

        for o in odds:
            inv_o = Decimal(1) / Decimal(o)
            f += inv_o ** c
            f_dash += (inv_o ** c) * (-inv_o.ln())  # Eftersom -ln(1/o) = ln(o)
        
        if abs(f_dash) < Decimal('1E-10'):
            st.warning("Numerisk instabilitet upptäckt, justerar exponentieringen.")
            fair_odds = [round(o / sum(1/o for o in odds), accuracy) for o in odds]
            return fair_odds
        
        # Korrekt Newton-uppdatering:
        h = f / f_dash
        c += h
        
        t = sum((Decimal(1) / Decimal(o)) ** c for o in odds)
        current_error = abs(t - Decimal(1) - target_overround)
        iteration_count += 1
    
    fair_odds = [round(float(o ** c), accuracy) for o in odds]
    return fair_odds
