import streamlit as st
from decimal import Decimal, getcontext

def get_no_vig_odds_multiway(odds, accuracy=3):
    """
    Beräknar no-vig (fair) odds baserat på inmatade odds.
    """
    # Ökar precisionen för beräkningar
    getcontext().prec = accuracy + 6

    # Kontroll: alla odds måste vara större än 1
    if any(o <= 1 for o in odds):
        st.error("Alla odds måste vara större än 1.")
        return []

    # Konvertera inmatade odds till Decimal för konsekvent beräkning
    odds_dec = [Decimal(str(o)) for o in odds]

    c = Decimal(1)
    target_overround = Decimal(0)
    current_error = Decimal(1000)
    max_error = Decimal(10) ** (-accuracy) / 2
    iteration_limit = 100  # Begränsning för att undvika oändliga loopar
    iteration_count = 0

    while current_error > max_error and iteration_count < iteration_limit:
        f = Decimal(-1 - target_overround)
        f_dash = Decimal(0)

        for o in odds_dec:
            inv_o = Decimal(1) / o
            # Beräkna f: summan av (1/o)^c - 1
            f += inv_o ** c
            # Beräkna derivatan f_dash:
            f_dash += (inv_o ** c) * (-inv_o.ln())  # Eftersom -ln(1/o) = ln(o)
        
        if abs(f_dash) < Decimal('1E-10'):
            st.warning("Numerisk instabilitet upptäckt, justerar exponentieringen.")
            # Proportionell metod vid instabilitet
            total = sum(Decimal(1) / o for o in odds_dec)
            fair_odds = [round(float(o / total), accuracy) for o in odds_dec]
            return fair_odds
        
        # Rätt Newton-uppdatering: h = f / f_dash (ej -f / f_dash)
        h = f / f_dash
        c += h
        
        t = sum((Decimal(1) / o) ** c for o in odds_dec)
        current_error = abs(t - Decimal(1) - target_overround)
        iteration_count += 1

    # Beräkna fair odds som exp(c * ln(o)) = o**c
    fair_odds = [round(float((o.ln() * c).exp()), accuracy) for o in odds_dec]
    return fair_odds

# Streamlit UI
st.title("No-Vig Odds Kalkylator 🎲")
st.write("Ange odds för en marknad och få fair odds utan bookmaker-marginal.")

odds_input = st.text_input("Ange odds separerade med komma (t.ex. 1.41, 4.2, 6.4, 22)")

if odds_input:
    try:
        odds = [float(o.strip()) for o in odds_input.split(",")]
        fair_odds = get_no_vig_odds_multiway(odds)
        if fair_odds:
            st.write("### Fair Odds")
            st.table({"Inmatade odds": odds, "Fair odds": fair_odds})
    except Exception as e:
        st.error(f"Ett fel uppstod: {e}")
