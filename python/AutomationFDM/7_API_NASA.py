import requests
import re
import os
from datetime import datetime

def validate_date(date_str):
    """Validate date format YYYY-MM-DD and ensure it's within APOD range."""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        min_date = datetime(1995, 6, 20)  # APOD start date
        max_date = datetime.now()
        if not (min_date <= date <= max_date):
            raise ValueError("Date must be between 1995-06-20 and today.")
        return date_str
    except ValueError as e:
        raise ValueError(f"Invalid date format or range: {e}")

def get_apod_data(date, api_key="DEMO_KEY"):
    """Fetch APOD data for the given date."""
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Error fetching APOD data: {e}")

def save_image(url, filename):
    """Download and save image from URL."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Saved image: {filename}")
    except requests.RequestException as e:
        print(f"Error downloading image: {e}")

def save_explanation(text, filename):
    """Save explanation text to file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Saved explanation: {filename}")
    except Exception as e:
        print(f"Error saving explanation: {e}")

def main():
    """Main function to get user input and process APOD data."""
    try:
        # Prompt user for date
        date = input("Enter date (YYYY-MM-DD): ").strip()
        date = validate_date(date)

        # Fetch APOD data
        data = get_apod_data(date)
        print(data)
        # Check if media type is image
        if data.get("media_type") != "image":
            print(f"Media for {date} is not an image (type: {data.get('media_type')}).")
            return

        # Get title and explanation
        title = data.get("title", "Untitled")
        explanation = data.get("explanation", "No explanation available")

        # Sanitize title for filename
        safe_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '_')

        # Create filenames
        image_filename = f"{date}-{safe_title}.jpg"
        explanation_filename = f"{date}-explanation.txt"

        # Save image and explanation
        save_image(data["url"], image_filename)
        save_explanation(explanation, explanation_filename)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()