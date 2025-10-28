import streamlit as st

def show_calculation_methodologies():
    """
    Displays the detailed explanations for how carbon footprints
    are calculated for each vehicle type in the EU.
    """
    
    # --- Car Methodology ---
    st.subheader("🚗 Car (Passenger Vehicle)")
    st.markdown("""
    - **Primary Metric:** `g/km` (grams of CO2 per kilometer).
    - **EU Methodology:** Since 2017, all new cars in the EU must be tested using the **`WLTP` (Worldwide Harmonised Light Vehicle Test Procedure)**.
    - **How it works:** WLTP is a laboratory test that simulates various driving conditions (urban, suburban, highway) to provide a more realistic `g/km` figure than the older NEDC test. This value is what manufacturers must report and is used for taxation and regulation.
    """)
    
    # --- Truck Methodology ---
    st.subheader("🚛 Truck (Heavy-Duty Vehicle - HDV)")
    st.markdown("""
    - **Primary Metric:** `g/t-km` (grams of CO2 per tonne-kilometer). This metric is more complex because it accounts for the *weight of goods* being transported.
    - **EU Methodology:** The EU uses a simulation tool called **`VECTO` (Vehicle Energy Consumption Calculation Tool)**.
    - **How it works:** Manufacturers must use VECTO to simulate the CO2 emissions and fuel consumption for various types of trucks and trailers based on their specific components (engine, tires, aerodynamics). This allows for a fair comparison of vehicles designed for different tasks. 
    - *Note: Our tool simplifies this to a `g/km` equivalent for demonstration.*
    """)
    
    # --- Motorcycle Methodology ---
    st.subheader("🏍️ Motorcycle")
    st.markdown("""
    - **Primary Metric:** `g/km` (grams of CO2 per kilometer).
    - **EU Methodology:** Emissions are tested as part of the **Euro 5** type-approval standards, using the **`WMTC` (World Motorcycle Test Cycle)**.
    - **How it works:** Similar to WLTP for cars, the WMTC is a standardized laboratory test cycle that simulates different riding phases to measure CO2, NOx, and other pollutants, resulting in an official `g/km` figure.
    """)
