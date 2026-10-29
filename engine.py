def estimate_ev_metrics(
    battery_kwh: float,
    soc_pct: float,
    base_wh_km: float,
    temp_c: float,
    ac_on: bool,
    music_on: bool,
    regen_mode: str  # "off", "standard", "aggressive"
) -> dict:
    """
    Computes real-time dynamic range and consumption based on real operating penalties.
    """
    # 1. Total available energy at current battery state of charge
    usable_energy_wh = (battery_kwh * (soc_pct / 100.0)) * 1000.0

    # 2. Ambient temperature efficiency modifier (eta_temp)
    # Optimum lithium-ion range is 20°C - 25°C
    if 20 <= temp_c <= 25:
        eta_temp = 1.00
    elif 10 <= temp_c < 20:
        eta_temp = 0.95
    elif 0 <= temp_c < 10:
        eta_temp = 0.88
    elif temp_c < 0:
        eta_temp = 0.76  # Freezing degradation + pack internal resistance
    elif 25 < temp_c <= 35:
        eta_temp = 0.96
    else:  # Severe heat (> 35°C) triggers aggressive coolant pumps
        eta_temp = 0.90

    # Effective base consumption under ambient temperature conditions
    effective_wh_km = base_wh_km / eta_temp

    # 3. Climate control / AC load
    # In extreme cold or extreme heat, thermal load spikes
    if ac_on:
        if temp_c > 35 or temp_c < 5:
            effective_wh_km += 32.0  # High HVAC compressor load
        else:
            effective_wh_km += 18.0  # Moderate cooling / heating

    # 4. Infotainment / Music draw
    if music_on:
        effective_wh_km += 3.5

    # 5. Regenerative braking recovery factor
    regen_multipliers = {
        "off": 1.00,
        "standard": 0.90,     # ~10% net energy savings in city/mixed driving
        "aggressive": 0.84    # ~16% energy recovered via one-pedal driving
    }
    effective_wh_km *= regen_multipliers.get(regen_mode.lower(), 1.00)

    # 6. Final predictions
    predicted_range = usable_energy_wh / effective_wh_km
    theoretical_factory_range = (battery_kwh * 1000.0) / base_wh_km
    range_delta_pct = ((predicted_range - theoretical_factory_range) / theoretical_factory_range) * 100

    return {
        "predicted_range_km": round(predicted_range, 1),
        "effective_consumption_wh_km": round(effective_wh_km, 1),
        "available_energy_kwh": round(usable_energy_wh / 1000.0, 2),
        "range_delta_vs_rated_pct": round(range_delta_pct, 1)
    }