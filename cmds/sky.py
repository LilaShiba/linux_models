#!/usr/bin/env python3

import requests

class Sky:
    """Class for fetching and displaying asteroid observations and NHATS data with magical emojis."""
    
    # Define some magical Sailor Moon-themed emojis for asteroid observations
    ASTEROID_EMOJIS = {
        "Observed": "🔭✨",
        "Close Approach": "🌍💫",
        "Bright": "🌟🌙",
        "Dim": "🌑💤",
        "Fast": "💨🚀",
        "Slow": "🐢🌠",
    }

    def __init__(self):
        """Initialize the class."""
        self.url = "https://ssd-api.jpl.nasa.gov/nhats.api?dv=6&dur=360&stay=8&launch=2020-2045&h=26&occ=7"

    def get_asteroid_emoji(self, magnitude, velocity):
        """Assign a Sailor Moon emoji based on brightness and speed."""
        # Ensure magnitude is numeric (convert to float if possible)
        try:
            magnitude = float(magnitude)
        except (ValueError, TypeError):
            magnitude = None

        if magnitude is not None and magnitude < 15:
            emoji = self.ASTEROID_EMOJIS["Bright"]
        elif magnitude is not None and magnitude > 20:
            emoji = self.ASTEROID_EMOJIS["Dim"]
        else:
            emoji = self.ASTEROID_EMOJIS["Observed"]

        # Handle velocity
        try:
            velocity = float(velocity)
        except (ValueError, TypeError):
            velocity = None
        
        if velocity is not None and velocity > 10:
            emoji += " " + self.ASTEROID_EMOJIS["Fast"]
        elif velocity is not None and velocity < 1:
            emoji += " " + self.ASTEROID_EMOJIS["Slow"]

        return emoji

    def fetch_nhats_data(self):
        """Fetch and display NHATS mission candidates."""
        try:
            print(f"🌍 Fetching NHATS data from: {self.url}")
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()

            if "data" in data:
                print(f"📡 Successfully fetched {len(data['data'])} NHATS missions.")
                return data["data"][:5]  # Limit to 5 results
            else:
                print("🌑 No NHATS mission candidates found!")
                return []

        except requests.exceptions.HTTPError as http_err:
            print(f"❌ HTTP error: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"❌ Request error: {req_err}")
        except Exception as e:
            print(f"❗ Unexpected error: {e}")
        
        return []

    def print_asteroid_observations(self, observations, top_n=10):
        """Print the latest asteroid observations in a magical format."""
        if not observations:
            print("🌑 No observations available to display.")
            return

        print("\n🌙✨ Latest Asteroid Observations ✨🌙\n")
        
        for i, obs in enumerate(observations[:top_n], start=1):
            # Extracting relevant data with fallbacks
            designation = obs.get("des", "Unknown")
            obs_start = obs.get("obs_start", "N/A")
            obs_end = obs.get("obs_end", "N/A")
            magnitude = obs.get("obs_mag", "N/A")
            min_dv = obs.get("min_dv", {}).get("dv", "N/A")
            max_size = obs.get("max_size", "N/A")
            n_via_traj = obs.get("n_via_traj", "N/A")
            emoji = self.get_asteroid_emoji(magnitude, min_dv)

            # Printing the observation details
            print(f"{i}. 🪐 {designation} {emoji}")
            print(f"   📅 Observation Period: {obs_start} to {obs_end}")
            print(f"   🔆 Magnitude: {magnitude}")
            print(f"   💨 Minimum Delta-V: {min_dv} km/s")
            print(f"   🌍 Max Size: {max_size} meters")
            print(f"   🌠 Trajectory Information: {n_via_traj} possible trajectory points")
            print("   ───────────────────────────")

    def main(self):
        """Main function to fetch and display asteroid observations and NHATS data."""
        print("🌍 Starting NHATS data fetch...")
        nhats_missions = self.fetch_nhats_data()

        if nhats_missions:
            print("🚀 Displaying observations:")
            self.print_asteroid_observations(nhats_missions)
        else:
            print("🌑 No new NHATS mission candidates available.")

if __name__ == "__main__":
    asteroid_observations = Sky()
    asteroid_observations.main()
