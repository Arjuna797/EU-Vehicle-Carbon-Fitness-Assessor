import streamlit as st

def render_header():
    """
    Displays the main title and introduction for the app.
    """
    st.title("EU Vehicle Carbon Fitness Assessor")
    st.markdown("""
    Welcome! This tool helps you assess if a vehicle is 'fit for the road' based on 
    simplified EU carbon emission standards. 
    
    Select a vehicle type, enter its CO2 emissions (in g/km), and see how it compares.
    """)

def render_result(is_fit, vehicle_type, user_input, threshold):
    """
    Displays a clear, color-coded result of the fitness assessment.
    
    Args:
        is_fit (bool): Whether the vehicle passed the check.
        vehicle_type (str): The category of vehicle (e.g., "Car").
        user_input (float): The g/km value entered by the user.
        threshold (float): The g/km standard for this vehicle type.
    """
    if is_fit:
        st.success(f"**Result: FIT FOR THE ROAD**")
        st.markdown(f"""
        Your **{vehicle_type}** (at **{user_input} g/km**) is **below** the simplified 
        EU standard of **{threshold} g/km**.
        
        This vehicle meets the target emission levels.
        """)
    else:
        st.error(f"**Result: NOT FIT FOR THE ROAD**")
        st.markdown(f"""
        Your **{vehicle_type}** (at **{user_input} g/km**) is **above** the simplified 
        EU standard of **{threshold} g/km**.
        
        This vehicle exceeds the target emission levels.
        """)

def render_footer():
    """
    Displays the footer with data source citations.
    """
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: grey;">
    <p>
    <strong>Disclaimer:</strong> This is a demonstration tool. 
    The emission standards used are simplified figures based on EU regulations 
    (e.g., Euro 5/6, EU 2019/631) for illustrative purposes.
    </p>
    <p>
    <strong>Data Source Concept:</strong> The thresholds are based on data published by the 
    <strong>European Environment Agency (EEA)</strong> and EU legislation. 
    A real-world application would connect to a live database of these standards, 
    such as those found on platforms like Kaggle (e.g., "CO2 emissions from new passenger cars in Europe").
    </p>
    </div>
    """, unsafe_allow_html=True)
