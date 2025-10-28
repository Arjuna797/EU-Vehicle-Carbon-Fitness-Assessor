# EU-Vehicle-Carbon-Fitness-Assessor
This Streamlit web application assesses whether a vehicle is 'fit for the road' based on its carbon footprint, with a specific focus on European Union (EU) standards. It also provides interactive visualizations of carbon emission trends across Europe.
# On Ubuntu / Linux
docker-compose up -d

# On Windows
docker compose up -d

📸 Application Preview

✨ Features

Vehicle Fitness Assessment:

Select a vehicle category (Car, Truck, Motorcycle).

Input the vehicle's carbon footprint (in g/km).

Receive an instant "Fit for Road" or "Not Fit for Road" result based on simplified EU standards.

Carbon Calculation Explained: An expandable section details how carbon footprints are generally calculated for each vehicle category.

EU Emissions Snapshot: A main-page summary of the top 5 EU countries with the highest CO2 emission reductions.

Interactive Data Visualization:

An interactive choropleth map of Europe showing CO2 reduction percentages between two user-selected years.

A dynamic bar chart displaying the top 15 countries by emission reduction for the selected period.

🛠 Tech Stack

Backend: Python

Frontend: Streamlit

Data Analysis: Pandas

Data Visualization: Plotly

Containerization: Docker & Docker Compose

📁 File Structure

Here is the layout of the project:

/eu-vehicle-app/
├── 📄 app.py               # Main application file, ties all modules together
├── 📄 ui_components.py      # Functions for Streamlit UI elements (header, etc.)
├── 📄 standards.py          # Contains the emission thresholds and logic
├── 📄 calculations.py       # Contains the text for the "How are footprints calculated?" section
├── 📄 data_visuals.py       # Handles data loading, processing, and Plotly graphs
├── 📄 eu_co2_emissions.csv  # The dataset file (must be added manually)
├── 📄 requirements.txt      # Python dependencies
├── 📄 Dockerfile            # Instructions for building the Docker image
├── 📄 docker-compose.yaml   # Service configuration for running with Docker
└── 📄 README.md             # This file


🚀 Getting Started

There are two methods to run this application. The Docker method is highly recommended as it handles all setup and dependencies automatically.

Method 1: Run with Docker (Recommended)

Prerequisites:

Docker Desktop installed and running.

Steps:

Clone the repository (or download all files):

git clone [https://github.com/your-username/eu-vehicle-app.git](https://github.com/your-username/eu-vehicle-app.git)
cd eu-vehicle-app


Get the Dataset (Crucial Step):

Download the dataset from Kaggle: CO2 Emissions (by country)

The downloaded file will be co2_emissions_kt_by_country.csv.

Rename this file to exactly eu_co2_emissions.csv.

Place the renamed file in the root of the project folder (alongside app.py).

Build and Run the Container:
Open your terminal and run:

docker-compose up --build


This command will build the Docker image, install all requirements.txt dependencies, and start the application.

View the App:
Open your web browser and go to: http://localhost:8080

Method 2: Run Locally (Manual Setup)

Clone the repository:




Create a Virtual Environment:

python -m venv venv
source venv/bin/activate  # On Mac/Linux
.\venv\Scripts\activate   # On Windows


Install Dependencies:

pip install -r requirements.txt


Get the Dataset (Crucial Step):

Follow Step 2 from the Docker instructions to download and rename the eu_co2_emissions.csv file.

Run Streamlit:

streamlit run app.py


View the App:
Streamlit will provide a local URL in your terminal, usually http://localhost:8501.

📊 Dataset

This application is designed to work with the CO2 Emissions (by country) dataset from Kaggle.

The data_visuals.py file is specifically configured to read the columns from this file:

country_name

year

value

If you use a different dataset, you must update the COUNTRY_COL, YEAR_COL, and VALUE_COL variables inside the load_data function in data_visuals.py.

📜 License

This project is licensed under the MIT License. See the LICENSE file for details.
