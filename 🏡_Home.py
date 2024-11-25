import streamlit as st
from datetime import datetime
import requests  # For API requests
import json
import os

# Path to the JSON file
DATA_FILE = "travel_data.json"

# Function to load data from JSON
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            'bucket_list': [],
            'trips_data': [],
            'reviews_data': [],
            'packing_list': []
        }

# Function to save data to JSON
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Load data from the JSON file
data = load_data()

# Initialize session state if not already done
if 'bucket_list' not in st.session_state:
    st.session_state.bucket_list = data['bucket_list']
if 'trips_data' not in st.session_state:
    st.session_state.trips_data = data['trips_data']
if 'reviews_data' not in st.session_state:
    st.session_state.reviews_data = data['reviews_data']
if 'packing_list' not in st.session_state:
    st.session_state.packing_list = data['packing_list']

# Apply dark mode CSS with full-page gradient
def set_dark_mode():
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(to right, #e74c3c, #f39c12);
            background-attachment: fixed;
            background-size: cover;
            color: #ffffff;
            font-family: 'Helvetica', sans-serif;
        }
        .stApp {
            background: transparent;
            padding: 0;
        }
        h1, h2, h3 {
            color: #ffffff;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8);
        }
        input, textarea, select, .stButton > button {
            background-color: #2c3e50 !important;
            color: #ffffff !important;
            border: 1px solid #34495e !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to save session data to the JSON file
def save_session_data():
    data = {
        'bucket_list': st.session_state.bucket_list,
        'trips_data': st.session_state.trips_data,
        'reviews_data': st.session_state.reviews_data,
        'packing_list': st.session_state.packing_list
    }
    save_data(data)

# Example: Modify a page that updates data (e.g., Bucket List page)
def bucket_list_page():
    set_dark_mode()
    st.markdown('<h1 style="text-align: center;">🌍 Travel Bucket List</h1>', unsafe_allow_html=True)

    st.subheader("✨ Your Dream Destinations")
    if not st.session_state.bucket_list:
        st.markdown('<p style="font-size: 18px; text-align: center;">No destinations added yet. Add some to your bucket list!</p>', unsafe_allow_html=True)
    else:
        for destination in st.session_state.bucket_list:
            if st.button(f"Learn about {destination}", key=f"explore_{destination}"):
                st.info(f"Fun fact about {destination}: A wonderful place to visit!")

    new_destination = st.text_input("Add New Destination", placeholder="E.g., Paris, Japan, Bali")
    if st.button("Add Destination"):
        if new_destination:
            st.session_state.bucket_list.append(new_destination)
            st.success(f"Added '{new_destination}' to your bucket list!")
            save_session_data()  # Save data after adding new destination
        else:
            st.error("Please enter a destination.")

# Trip Planner Page
def trip_planner_page():
    set_dark_mode()
    st.markdown('<h1 style="text-align: center;">📅 Plan Your Trip</h1>', unsafe_allow_html=True)

    destination = st.selectbox("Select Destination", st.session_state.bucket_list, help="Choose a destination")
    date_range = st.date_input("Select Travel Dates", [datetime.today(), datetime.today()])

    notes = st.text_area("Add Notes for the Trip")
    if st.button("Save Trip"):
        st.session_state.trips_data.append({"destination": destination, "dates": date_range, "notes": notes})
        st.success(f"Saved your trip to {destination}!")
        save_session_data()  # Save data after saving a trip

# Reviews Page
def reviews_ratings_page():
    set_dark_mode()
    st.markdown('<h1 style="text-align: center;">⭐ Reviews & Ratings</h1>', unsafe_allow_html=True)

    destination = st.selectbox("Select Destination", st.session_state.bucket_list, help="Choose a destination")
    rating = st.slider("Rate the destination (1-5)", 1, 5)
    review_text = st.text_area("Write your review")

    if st.button("Submit Review"):
        st.session_state.reviews_data.append({"destination": destination, "rating": rating, "review": review_text})
        st.success(f"Thanks for reviewing {destination}!")
        save_session_data()  # Save data after submitting a review

# Currency Converter Page
def currency_converter_page():
    set_dark_mode()
    st.markdown('<h1 style="text-align: center;">💱 Currency Converter</h1>', unsafe_allow_html=True)

    st.subheader("Convert Between Currencies")
    from_currency = st.text_input("From Currency (e.g., USD)")
    to_currency = st.text_input("To Currency (e.g., EUR)")
    amount = st.number_input("Amount to Convert", min_value=0.0, step=1.0)

    if st.button("Convert"):
        if from_currency and to_currency and amount > 0:
            try:
                # Replace 'YOUR_API_KEY' with an actual API key
                response = requests.get(
                    f"https://v6.exchangerate-api.com/v6/e085548ce220b4416e8f361d/latest/{from_currency}"
                )
                data = response.json()
                if response.status_code == 200:
                    rate = data['conversion_rates'].get(to_currency.upper())
                    if rate:
                        converted = amount * rate
                        st.success(f"{amount} {from_currency.upper()} = {converted:.2f} {to_currency.upper()}")
                    else:
                        st.error("Invalid target currency.")
                else:
                    st.error("Failed to fetch exchange rates.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please fill in all fields.")


# Weather Forecast Page
def weather_forecast_page():
    set_dark_mode()
    st.markdown('<h1 style="text-align: center;">🌤️ Weather Forecast</h1>', unsafe_allow_html=True)

    destination = st.text_input("Enter Destination City", placeholder="E.g., Tokyo, New York")

    if st.button("Get Weather"):
        if destination:
            try:
                # Step 1: Use OpenCage to get latitude and longitude
                geocode_url = f"https://api.opencagedata.com/geocode/v1/json?q={destination}&key=1b24b6c685df49ee87bafd497740d10e"
                geo_response = requests.get(geocode_url)
                geo_data = geo_response.json()

                if geo_response.status_code == 200 and geo_data['results']:
                    lat = geo_data['results'][0]['geometry']['lat']
                    lng = geo_data['results'][0]['geometry']['lng']

                    # Step 2: Use OpenWeatherMap to get the weather forecast (still using OpenWeatherMap)
                    api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
                    weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lng}&units=metric&appid={api_key}"
                    weather_response = requests.get(weather_url)
                    weather_data = weather_response.json()

                    if weather_response.status_code == 200:
                        st.success(f"7-day Weather Forecast for {destination.capitalize()}:")
                        for day in weather_data['list'][:7]:
                            date = day['dt_txt']
                            temp = day['main']['temp']
                            weather = day['weather'][0]['description']
                            st.write(f"**{date}** - Temp: {temp}°C, {weather.capitalize()}")
                    else:
                        st.error("Failed to fetch weather data. Please try again later.")
                else:
                    st.error(f"Could not find the location '{destination}'. Please check the spelling.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a destination.")

# Nearby Attractions Page
def get_coordinates(location):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key=1b24b6c685df49ee87bafd497740d10e"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and data['results']:
        lat = data['results'][0]['geometry']['lat']
        lng = data['results'][0]['geometry']['lng']
        return lat, lng
    else:
        return None

# Function to fetch nearby attractions using Overpass API (OpenStreetMap)
def fetch_nearby_attractions(lat, lng):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node["tourism"](around:5000, {lat}, {lng});
      way["tourism"](around:5000, {lat}, {lng});
      relation["tourism"](around:5000, {lat}, {lng});
    );
    out body;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()

    attractions = []
    for element in data['elements']:
        if 'tags' in element:
            name = element['tags'].get('name', 'Unknown')
            attractions.append(name)

    return attractions

# Nearby Attractions Page
def nearby_attractions_page():
    set_dark_mode()
    st.markdown('<h1 style="text-align: center;">🏞️ Nearby Attractions</h1>', unsafe_allow_html=True)

    location = st.text_input("Enter Destination (City/Location)", placeholder="E.g., Paris, London, New York")

    if location:
        if st.button("Search Attractions"):
            st.info("Searching for attractions... Please wait.")
            coords = get_coordinates(location)
            if coords:
                lat, lng = coords
                attractions = fetch_nearby_attractions(lat, lng)
                if attractions:
                    st.subheader(f"Top Attractions near {location}:")
                    for idx, attraction in enumerate(attractions[:5]):  # Limit to top 5 attractions
                        st.write(f"**{idx + 1}. {attraction}**")
                    st.markdown("---")
                else:
                    st.error(f"No attractions found for {location}. Please try another location.")
            else:
                st.error(f"Could not find coordinates for {location}. Please try again.")
    else:
        st.warning("Please enter a location to search for attractions.")


# Packing Checklist Page
def packing_checklist_page():
    set_dark_mode()
    st.markdown('<h1 style="text-align: center;">🎒 Packing Checklist</h1>', unsafe_allow_html=True)

    st.subheader("Create Your Packing Checklist")
    new_item = st.text_input("Add Item")
    if st.button("Add Item"):
        if new_item:
            st.session_state.packing_list.append({"item": new_item, "packed": False})
            st.success(f"Added '{new_item}' to your checklist!")
            save_session_data()  # Save data after adding item
        else:
            st.error("Please enter an item.")

    st.subheader("Your Checklist")
    for idx, item in enumerate(st.session_state.packing_list):
        col1, col2 = st.columns([3, 1])
        col1.markdown(f"- {item['item']}")
        if col2.checkbox("Packed", key=f"packed_{idx}"):
            st.session_state.packing_list[idx]['packed'] = True
            save_session_data()  # Save data when checking off an item


# Main function
def main():
    st.sidebar.title("Travel App")
    page = st.sidebar.radio(
        "Navigate",
        [
            "Bucket List",
            "Trip Planner",
            "Reviews & Ratings",
            "Currency Converter",
            "Weather Forecast",
            "Nearby Attractions",
            "Packing Checklist",
        ],
    )

    if page == "Bucket List":
        bucket_list_page()
    elif page == "Trip Planner":
        trip_planner_page()
    elif page == "Reviews & Ratings":
        reviews_ratings_page()
    elif page == "Currency Converter":
        currency_converter_page()
    elif page == "Weather Forecast":
        weather_forecast_page()
    elif page == "Nearby Attractions":
        nearby_attractions_page()
    elif page == "Packing Checklist":
        packing_checklist_page()

if __name__ == "__main__":
    main()
