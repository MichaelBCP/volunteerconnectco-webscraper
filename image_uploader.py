import requests
from dotenv import load_dotenv
import os

def upload_to_imgbb(image_url):
    load_dotenv()
    imgbb_api_key = os.getenv('IMGBB_API_KEY')

    try:
        img_data = requests.get(image_url).content
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            params={'key': imgbb_api_key},
            files={'image': img_data}
        )
        response.raise_for_status()
        return response.json()['data']['url']
    except Exception as e:
        return f"Image upload failed: {e}"

if __name__ == '__main__':
    img_url = upload_to_imgbb("https://scrapepark.org/images/slider-bg.jpg")
    print(img_url)