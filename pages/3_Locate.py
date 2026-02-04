import requests
import streamlit as st
from geopy.geocoders import Nominatim
from typing import TypedDict

st.set_page_config(
    page_title="Skin Cancer Detection | Locate",
    page_icon="♋",
    layout="centered",
    initial_sidebar_state="expanded",
)


st.title("Find a dermatologist")
# Set the location and radius for the search
city = (
    st.text_input(
        label="Enter your city",
        placeholder="City (e.g. New Delhi)",
        help="Enter the name of the city where you want to find a dermatologist",
    )
    .strip()
    .title()
)


class Dermatologist(TypedDict):
    name: str
    address: str


if st.button("Find a dermatologist"):
    if not city:
        st.error("Please enter a city")
        st.stop()
    api_key = st.secrets["GOOGLE_API_KEY"]
    if not api_key:
        st.error("Please set the GOOGLE_API_KEY secret")
        st.stop()

    # Create a geolocator object
    geolocator = Nominatim(user_agent="skin_cancer")

    # Use the geolocator to get the latitude and longitude of the city
    location = geolocator.geocode(city)
    latitude = location.latitude
    longitude = location.longitude

    location = f"{latitude},{longitude}"
    RADIUS = 10000  # 10 km
    KEYWORD = "dermatologist"

    # Make the request to the Places API
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={RADIUS}&keyword={KEYWORD}&key={api_key}"
    response = requests.get(url, timeout=10)
    results = response.json()["results"]

    # Extract the place IDs of the results
    place_ids = [result["place_id"] for result in results]

    # Use the place IDs to get the details of the places
    dermatologists: list[Dermatologist] = []
    for place_id in place_ids:
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
        response = requests.get(url, timeout=10)
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
        with st.expander(dermatologist["name"]):
            st.markdown(f"**Address:** {dermatologist['address']}")
