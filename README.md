# ⚡ Dynamic EV Range & Battery Efficiency Estimator

A physics-based electric vehicle range prediction dashboard that calculates real-world distance-to-empty based on battery pack capacity, ambient temperature degradation, auxiliary cabin loads, and regenerative braking.

---

## 🚀 Features
- **Vehicle Database:** Includes 25+ EVs (Tata, Tesla, Mahindra, MG, Hyundai, BYD, etc.).
- **Thermal Efficiency Modeling:** Simulates electrochemical lithium-ion performance drops in extreme cold (<0°C) and hot weather (>35°C).
- **Parasitic Load Calculations:** Models HVAC compressor and infotainment power draw in Wh/km.
- **Energy Regeneration:** Adjusts consumption savings based on regenerative braking intensity.

---

## 🛠️ Tech Stack
- **Language:** Python
- **Framework:** Streamlit
- **Data Source:** Curated EV specifications (usable kWh, rated Wh/km, test-cycle range)

---

## 📦 Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/ev-range-estimator.git
   cd ev-range-estimator
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the app:**
   ```bash
   streamlit run app.py
   ```

---

## 📐 Mathematical Formulation

$$\text{Estimated Range (km)} = \frac{\text{Available Energy (Wh)}}{\text{Effective Consumption (Wh/km)}}$$

Where:
$$\text{Effective Consumption} = \left(\frac{C_{\text{base}}}{\eta_{\text{temp}}} + \Delta C_{\text{AC}} + \Delta C_{\text{info}}\right) \times \lambda_{\text{regen}}$$
