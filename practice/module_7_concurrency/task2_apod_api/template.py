import requests
import os
from concurrent.futures import ThreadPoolExecutor

API_KEY = "YOUR_KEY"
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_IMAGES = os.path.join(os.path.dirname(os.path.abspath(__file__)), './output')

def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:
    url = f"{APOD_ENDPOINT}?api_key={api_key}&start_date={start_date}&end_date={end_date}"
    response_jsons = requests.get(url).json()
    photos_urls = []
    for r in response_jsons:
        if r["media_type"] == "image":
            photo_url = {"date": r["date"], "url": r["url"]}
            photos_urls.append(photo_url)
    return photos_urls

def scrape(args):
    date, url = args
    response = requests.get(url)
    print(response)
    with open(f"{OUTPUT_IMAGES}/nasa_image_{date}.jpg", "wb") as f:
        f.write(response.content)
    print(f"Image downloaded!: nasa_image_{date}.jpg")

def download_apod_images(metadata: list):
    os.makedirs(OUTPUT_IMAGES, exist_ok=True)
    with ThreadPoolExecutor() as executor:
        executor.map(scrape, [(m["date"], m["url"]) for m in metadata])


def main():
    metadata = get_apod_metadata(
        start_date='2021-08-01',
        end_date='2021-09-30',
        api_key=API_KEY,
    )
    download_apod_images(metadata=metadata)


if __name__ == '__main__':
    main()
