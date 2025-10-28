import streamlit as st
import pandas as pd
import plotly.express as px

# Define a consistent list of EU/Europe countries for filtering.
# This list is more comprehensive to match the new dataset.
EUROPEAN_COUNTRIES = [
    'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia and Herzegovina',
    'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 
    'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland',
    'Italy', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg',
    'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia',
    'Norway', 'Poland', 'Portugal', 'Romania', 'Russian Federation', 'San Marino', 'Serbia',
    'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 
    'United Kingdom'
]

@st.cache_data
def load_data(csv_path):
    """
    Loads and caches the CO2 emission data from a CSV file.
    This version is specifically adjusted for the Kaggle dataset:
    'co2_emissions_kt_by_country.csv'
    """
    # --- ADJUST COLUMN NAMES HERE ---
    # Updated to match 'co2_emissions_kt_by_country.csv'
    COUNTRY_COL = 'country_name'  # Was 'geo'
    YEAR_COL = 'year'             # Was 'time'
    VALUE_COL = 'value'           # Was 'values'
    # --------------------------------
    
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        # This is the first check. If the file isn't found, stop.
        st.error(f"**Data file not found:** The file `{csv_path}` was not found in your project directory.")
        st.info(f"Please follow these steps:\n"
                f"1. Download the CSV from: https://www.kaggle.com/datasets/ulrikthygepedersen/co2-emissions-by-country\n"
                f"2. Rename the downloaded file to exactly `eu_co2_emissions.csv`.\n"
                f"3. Place it in the same folder as `app.py`.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred reading the CSV file: {e}")
        return pd.DataFrame()

    # Basic data cleaning: rename columns to our standard names
    df = df.rename(columns={
        COUNTRY_COL: 'Country Name',
        YEAR_COL: 'Year',
        VALUE_COL: 'Emissions'
    })
    
    # Ensure required columns exist *after* renaming
    if not all(col in df.columns for col in ['Country Name', 'Year', 'Emissions']):
        st.error(f"**Dataset Column Mismatch!**")
        st.warning(f"The file `{csv_path}` was found, but it does not contain the expected columns: `{COUNTRY_COL}`, `{YEAR_COL}`, and `{VALUE_COL}`.")
        st.info("Please ensure you downloaded the correct file from the link provided.")
        return pd.DataFrame()

    # Convert year to numeric, coercing errors
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    # The new dataset has emissions as 'kt' (kilotons), which is fine
    df['Emissions'] = pd.to_numeric(df['Emissions'], errors='coerce')
    
    # Filter for relevant European countries
    # We must clean the country names from the CSV to match our list
    df['Country Name'] = df['Country Name'].str.strip() # Remove any whitespace
    df = df[df['Country Name'].isin(EUROPEAN_COUNTRIES)]
    
    # Drop any rows that failed conversion or are missing data
    df = df.dropna(subset=['Year', 'Emissions', 'Country Name'])
    
    # Convert year to integer
    df['Year'] = df['Year'].astype(int)
    
    return df

def calculate_reduction(df, start_year, end_year):
    """
    Calculates the percentage reduction in emissions between two years.
    """
    # Group by country and year, summing emissions
    df_agg = df.groupby(['Country Name', 'Year'])['Emissions'].sum().reset_index()

    df_start = df_agg[df_agg['Year'] == start_year][['Country Name', 'Emissions']].rename(columns={'Emissions': 'Start Emissions'})
    df_end = df_agg[df_agg['Year'] == end_year][['Country Name', 'Emissions']].rename(columns={'Emissions': 'End Emissions'})
    
    df_merged = pd.merge(df_start, df_end, on='Country Name')
    
    if df_merged.empty:
        return pd.DataFrame(columns=['Country Name', 'Percentage Reduction'])

    # Calculate percentage reduction
    df_merged['Percentage Reduction'] = (
        (df_merged['Start Emissions'] - df_merged['End Emissions']) / df_merged['Start Emissions']
    ) * 100
    
    # Handle potential division by zero
    df_merged = df_merged.replace([float('inf'), float('-inf')], pd.NA).dropna(subset=['Percentage Reduction'])
    
    return df_merged[['Country Name', 'Percentage Reduction']]

def create_choropleth_map(df, start_year, end_year):
    """
    Creates an interactive Plotly choropleth map.
    """
    fig = px.choropleth(
        df,
        locations="Country Name",
        locationmode="country names",
        color="Percentage Reduction",
        hover_name="Country Name",
        scope="europe",
        title=f"CO2 Emission Reduction ({start_year} vs {end_year})",
        # --- THIS IS THE FIX ---
        color_continuous_scale=px.colors.diverging.RdYlGn, # Red-Yellow-Green
        # ---------------------
        labels={'Percentage Reduction': '% Reduction'}
    )
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig

def create_bar_chart(df):
    """
    Creates an interactive Plotly bar chart of top reducers.
    """
    df_sorted = df.sort_values(by="Percentage Reduction", ascending=False).head(15)
    fig = px.bar(
        df_sorted,
        x="Country Name",
        y="Percentage Reduction",
        title="Top 15 Countries by Emission Reduction",
        labels={'Percentage Reduction': '% Reduction'},
        color="Percentage Reduction",
        # Using a sequential scale here is correct, as it's all positive
        color_continuous_scale=px.colors.sequential.Greens
    )
    return fig

def render_graphs():
    """
    Main function to render the graphs section in the Streamlit app.
    """
    st.header("EU Region Carbon Footprint Trends")
    st.markdown("""
    This section visualizes the change in total CO2 emissions by country over time, 
    based on data sourced from Kaggle.
    """)
    
    csv_file = 'eu_co2_emissions.csv'
    
    # Load_data() will now handle showing the specific errors
    df = load_data(csv_file)
    
    if df.empty:
        st.warning("Data could not be loaded. Please check the error messages above.")
        return

    all_years = sorted(df['Year'].unique())
    
    if len(all_years) < 2:
        st.warning("The dataset needs at least two different years of data to compare.")
        return

    # Interactive sliders for year selection
    start_year, end_year = st.select_slider(
        "Select year range to compare:",
        options=all_years,
        value=(all_years[0], all_years[-1]) # Default to first and last year
    )
    
    if start_year >= end_year:
        st.warning("Start year must be before end year.")
        return

    reduction_df = calculate_reduction(df, start_year, end_year)
    
    if reduction_df.empty:
        st.warning(f"No data available for both {start_year} and {end_year}. Try a different year range.")
    else:
        # Display the interactive graphs
        fig_map = create_choropleth_map(reduction_df, start_year, end_year)
        st.plotly_chart(fig_map, use_container_width=True)
        
        fig_bar = create_bar_chart(reduction_df)
        st.plotly_chart(fig_bar, use_container_width=True)

