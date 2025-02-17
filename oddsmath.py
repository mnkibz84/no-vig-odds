import math
from decimal import Decimal, getcontext

def get_no_vig_odds_multiway(odds: list, accuracy=3):
    """
    :param odds: List of original odds for a multi-way market.
    :param accuracy: Decimal precision for fair odds calculation.
    :return: List of no-vig (fair) odds.
    """
    # Sätt decimalprecision
    getcontext().prec = accuracy + 2
    
    # Kontrollera ogiltiga odds
    if any(o <= 1 for o in odds):
        raise ValueError("Alla odds måste vara större än 1.")
    
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
        
        # Uppdatera felet
        t = sum((Decimal(1) / Decimal(o)) ** c for o in odds)
        current_error = abs(t - Decimal(1) - target_overround)
    
    # Beräkna slutliga fair odds
    fair_odds = [round(float(Decimal(o) ** c), accuracy) for o in odds]
    return fair_odds

# Testkörning
print(get_no_vig_odds_multiway([1.41, 4.2, 6.4, 22], accuracy=4))
