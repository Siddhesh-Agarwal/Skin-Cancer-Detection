import streamlit as st
from geopy.geocoders import Nominatim
import requests

st.set_page_config(
    page_title="Skin Cancer",
    page_icon="♋",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Replace YOUR_API_KEY with your actual API key
api_key = st.secrets["api_key"]


st.title("Find a dermatologist")
# Set the location and radius for the search
city = st.text_input(
    label="Enter your city",
    placeholder="City (e.g. New Delhi)",
    help="Enter the name of the city where you want to find a dermatologist",
).strip()

if city != "":
    # Create a geolocator object
    geolocator = Nominatim(user_agent="skin_cancer")

    # Use the geolocator to get the latitude and longitude of the city
    location = geolocator.geocode(city)
    latitude = location.latitude
    longitude = location.longitude

    location = f"{latitude},{longitude}"
    radius = 10000  # 10 km
    keyword = "dermatologist"

    # Make the request to the Places API
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&keyword={keyword}&key={api_key}"
    response = requests.get(url)
    results = response.json()["results"]

    # Extract the place IDs of the results
    place_ids = [result["place_id"] for result in results]

    # Use the place IDs to get the details of the places
    dermatologists = []
    for place_id in place_ids:
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
        response = requests.get(url)
        place_details = response.json()["result"]
        dermatologists.append(
            {
                "name": place_details["name"],
                "address": place_details["formatted_address"],
            }
        )

    # Display the results in Streamlit
    st.header("Results")
    for i, dermatologist in enumerate(dermatologists, start=1):
        # st.markdown(f"**{dermatologist['name']}**")
        # st.markdown(dermatologist["address"])
        st.markdown(
            f"""
            {i}. **{dermatologist['name']}**
            > **Address:** {dermatologist['address']}
            """
        )
