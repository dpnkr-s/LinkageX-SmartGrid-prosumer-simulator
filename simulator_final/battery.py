# Battery function
def battery(soc, capacity, p_gen, p_load):
        
        old_soc = soc
        # available energy in battery: Wh
        available = soc * capacity 
        # PV energy generated during this hour: Wh
        generated = p_gen
        # Energy consumed by loads during this hour: Wh
        consumed = p_load
        # Power balance
        diff = available + generated - consumed
        # Base SOC calculation: Wh / Wh -> percentage
        soc = (diff) / capacity 
        # Bound between 0 and 100 %
        if soc > 1.0:
            soc = 1.0
        elif soc < 0:
            soc = 0.0
        # trapezoid rule: integral(W * dt, t=hour_i..hour_i+1) = 1 * (W_i+1 - W_i)/2 [units: W*h]
        soc = (soc + old_soc)/2.0 
        return soc, diff