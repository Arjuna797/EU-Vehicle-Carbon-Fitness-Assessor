import streamlit as st
import pandas as pd
import standards
import calculations
import ui_components
import data_visuals  # Import the new module

# --- Page Configuration ---
st.set_page_config(
    page_title="EU Vehicle Carbon Fitness",
    page_icon="🇪🇺",
    layout="wide"
)

def render_top_reducers_preview():
    """
    Renders a small preview section showing the top 5 countries
    for carbon reduction, based on the loaded CSV data.
    """
    st.subheader("EU Emissions Snapshot")
    
    csv_file = 'eu_co2_emissions.csv'
    
    try:
        # We can re-use the cached load_data function from data_visuals
        df = data_visuals.load_data(csv_file)
        
        if df.empty:
            st.info("Add the 'eu_co2_emissions.csv' file to see emission reduction leaders.")
            return

        all_years = sorted(df['Year'].unique())
        
        if len(all_years) < 2:
            st.info("Dataset needs more than one year of data to show reductions.")
            return

        # Automatically compare the first and last year in the dataset
        start_year, end_year = all_years[0], all_years[-1]
        
        reduction_df = data_visuals.calculate_reduction(df, start_year, end_year)
        
        if reduction_df.empty:
            st.warning(f"Could not calculate reductions between {start_year} and {end_year}.")
        else:
            top_5 = reduction_df.sort_values(by="Percentage Reduction", ascending=False).head(5)
            
            with st.container(border=True):
                st.markdown(f"**Top 5 Reducers** (Change from {start_year} to {end_year})")
                
                # Display the top 5 in a clean way
                for index, row in top_5.iterrows():
                    st.markdown(f"1. **{row['Country Name']}**: {row['Percentage Reduction']:.1f}% reduction")
                
                st.markdown("\n*Scroll down for detailed interactive graphs!* 👇")

    except FileNotFoundError:
        st.info("Add the 'eu_co2_emissions.csv' dataset to view emission reduction leaders.")
    except Exception as e:
        st.error(f"Error loading snapshot: {e}")

# --- Main Application UI ---
def main():
    """
    Renders the main application interface, handles user input,
    and displays assessment results.
    """
    
    # Render the header section from our UI module
    ui_components.render_header()

    # Create two main columns for a clean layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Check Your Vehicle's Fitness")
        
        # Use a container for a visually distinct input area
        with st.container(border=True):
            # 1. Vehicle Category Selection
            vehicle_type = st.selectbox(
                "1. Select Vehicle Category",
                ("Car", "Truck", "Motorcycle"),
                index=0,  # Default to 'Car'
                help="Choose the type of vehicle you want to assess."
            )

            # 2. Carbon Footprint Input
            carbon_footprint = st.number_input(
                f"2. Enter Carbon Footprint (g/km)",
                min_value=0.0,
                value=100.0,  # Sensible default
                step=0.1,
                format="%.2f",
                help=f"Enter the official CO2 emission value for your {vehicle_type.lower()} in grams per kilometer (g/km)."
            )

            # 3. Assessment Button
            if st.button("Assess Fitness", type="primary", use_container_width=True):
                # When clicked, perform the assessment
                if vehicle_type and carbon_footprint is not None:
                    # Call the logic from our 'standards' module
                    is_fit, threshold = standards.check_fitness(vehicle_type, carbon_footprint)
                    
                    # Store the result in session state to display it in the other column
                    st.session_state.result = {
                        "is_fit": is_fit,
                        "threshold": threshold,
                        "user_input": carbon_footprint,
                        "vehicle_type": vehicle_type
                    }
                else:
                    st.warning("Please enter a valid carbon footprint value.")
    
    with col2:
        st.subheader("Assessment Result")
        
        # Display the result if it's in the session state
        if 'result' in st.session_state:
            res = st.session_state.result
            ui_components.render_result(
                res["is_fit"],
                res["vehicle_type"],
                res["user_input"],
                res["threshold"]
            )
        else:
            # Placeholder before the first assessment
            st.info("Your assessment result will appear here.")

    # --- NEW: Top Reducers Preview Section ---
    st.divider()
    render_top_reducers_preview()
    # -----------------------------------------

    st.divider()

    # --- Calculation Methodology Section ---
    with st.expander("How are Carbon Footprints Calculated in the EU?"):
        st.write("""
        The "carbon footprint" for vehicles in the EU is typically measured in **grams of CO2 per kilometer (g/km)**. 
        This figure is determined through standardized testing procedures designed to simulate real-world driving. 
        The specific methodology varies by vehicle type.
        """)
        
        # Render the explanations from our 'calculations' module
        calculations.show_calculation_methodologies()

    # --- Data Visualization Section (Existing) ---
    st.divider()
    data_visuals.render_graphs()
    # -------------------------------------------

    # --- Footer ---
    ui_components.render_footer()

if __name__ == "__main__":
    main()

