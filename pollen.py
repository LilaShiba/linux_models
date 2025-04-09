#!/usr/bin/env python3

import requests
import sys
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the Ambee API key from the environment variable
API_KEY = os.getenv("POLLEN")  # Replace with your actual variable name in .env file
if not API_KEY:
    print("❌ API key not found. Please add 'POLLEN_API_KEY' in your .env file.")
    sys.exit(1)

GEO_URL = "https://nominatim.openstreetmap.org/search"
POLLEN_URL = "https://api.ambeedata.com/latest/pollen/by-lat-lng"

# Emoji dictionary for different types of allergens
ALLERGEN_EMOJIS = {
    "Grass": "🌱",  # Grass pollen
    "Tree": "🌳",   # Tree pollen
    "Weed": "🌾",   # Weed pollen
}

def get_coordinates(city_name):
    """Convert city name to coordinates using Nominatim with required User-Agent."""
    headers = {
        "User-Agent": "cli-tools/1.0 (Lila James; pollen@local.test)"  # Adding User-Agent header to avoid rate-limiting issues
    }
    params = {"q": city_name, "format": "json"}
    response = requests.get(GEO_URL, params=params, headers=headers)

    try:
        results = response.json()
    except Exception as e:
        print(f"❌ Failed to decode response from geocoder: {e}")
        print(f"↪ Response content: {response.text}")
        return None, None

    if not results:
        print(f"❌ Could not find coordinates for {city_name}")
        return None, None

    return float(results[0]["lat"]), float(results[0]["lon"])

def fetch_pollen_data(lat, lng):
    """Fetch pollen data from Ambee API."""
    headers = {"x-api-key": API_KEY}
    params = {"lat": lat, "lng": lng}
    response = requests.get(POLLEN_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error fetching pollen data: {response.status_code}")
        return {}

def display_pollen_data(data, lat, lon):
    """Display pollen data in a user-friendly format with top allergens based on species."""
    pollen_info = data.get("data", [])[0] if data.get("data") else {}
    if not pollen_info:
        print("❌ No pollen data available.")
        return

    updated_at = pollen_info.get('updatedAt', 'N/A')

    # Getting the species counts for each type
    species = pollen_info.get("Species", {})
    risk = pollen_info.get("Risk", {})
    counts = pollen_info.get("Count", {})

    print(f"\n📍 Location: Latitude {lat}, Longitude {lon}")
    print(f"📅 Date: {updated_at}")
    print("\n🌿 Top Allergens:")

    # Process Grass, Tree, and Weed species and display the top 2 allergens
    for category, allergens in species.items():
        print(f"\n🔖 {category}:")
        
        # Check if allergens is a dictionary or an integer
        if isinstance(allergens, dict):
            # Sort allergens by count and get top 2
            sorted_allergens = sorted(allergens.items(), key=lambda x: x[1], reverse=True)[:2]
            
            for allergen, count in sorted_allergens:
                emoji = ALLERGEN_EMOJIS.get(category, "❓")
                risk_level = risk.get(f"{category.lower()}_pollen", "N/A")
                print(f"   {emoji} {allergen}: {count} grains/m³ (Risk: {risk_level})")
        
        # If the allergens is a number (like "Grass / Poaceae")
        else:
            emoji = ALLERGEN_EMOJIS.get(category, "❓")
            risk_level = risk.get(f"{category.lower()}_pollen", "N/A")
            print(f"   {emoji} {category}: {allergens} grains/m³ (Risk: {risk_level})")

def main():
    if len(sys.argv) < 2:
        print("Usage: pollen <City Name>")
        return

    city = " ".join(sys.argv[1:])
    lat, lng = get_coordinates(city)
    if lat is not None and lng is not None:
        data = fetch_pollen_data(lat, lng)
        display_pollen_data(data, lat, lng)

if __name__ == "__main__":
    main()
