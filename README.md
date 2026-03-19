# Steam Library Analysis Dashboard

**Live Demo:** [Click here to view the live dashboard]([LINK](https://steamlibrarydashboard-bc99vjmfpwi24e6jpdmfvm.streamlit.app/))

## Project Overview
The Steam Library Analyst is an interactive data visualization dashboard built with Python and Streamlit. It connects to the Steam Web API to fetch, clean, and analyze a user's gaming data. The application processes JSON data to provide insights into gaming habits, top-played titles, and overall library statistics.

## Features
* **Live API Integration:** Fetches real-time library data using the Steam Web API.
* **Data Transformation:** Utilizes Pandas to convert raw API data and dynamically generate game cover-art URLs.
* **Interactive Visualizations:** Displays top-played games using Streamlit bar charts.
* **Data Tables:** Presents an interactive dataframe featuring game cover art, titles, and formatted playtime metrics.
* **Secure Credentials:** Implements Streamlit Secrets Management to handle private API keys.

## Technologies Used
* **Language:** Python
* **Framework:** Streamlit
* **Data Manipulation:** Pandas
* **API Requests:** Requests library

## Local Installation

To run this dashboard locally, follow these steps:

**1. Clone the repository**
git clone [https://github.com/Kolek88/steamlibrary_dashboard.git](https://github.com/Kolek88/steamlibrary_dashboard.git)
cd steamlibrary_dashboard

**2. Install dependencies**
pip install -r requirements.txt

**3. Configure Credentials**
-Create a directory named .streamlit in the root folder.
-Inside .streamlit, create a file named secrets.toml.
-Add your Steam API credentials to the file:
  STEAM_API_KEY = "Your-API-Key-Here"
  STEAM_ID = "Your-Steam-ID-Here"

  **4. Run the application**
  streamlit run steam_app.py
