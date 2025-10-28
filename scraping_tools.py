import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from image_uploader import *

def get_text_from_url(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # Check for request errors

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator="\n", strip=True)
        linksChecked = 0
        print("check1")
        for a in soup.find_all('a'):
            if linksChecked <= 5:
                href = a.get("href")
                if href:
                    response = requests.get((urljoin(url, href)), headers = {'User-Agent': 'Mozilla/5.0'})
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text += soup.get_text(separator="\n", strip=True)
                    linksChecked += 1
        print(text)
        return text
    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}"



def get_img_from_url(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')

        valid_exts = ('.png', '.jpg', '.jpeg', '.webp')
        fallback_img = None

        for img in images:
            src = img.get('src')
            if not src:
                continue

            full_url = urljoin(url, src)

            if full_url.lower().endswith(valid_exts):
                return full_url  # Found usable image
            elif not fallback_img:
                fallback_img = full_url  # Save first fallback

        # No usable image found; try uploading fallback to ImgBB
        if fallback_img:
            return upload_to_imgbb(fallback_img)

        return "No usable image found and no fallback available."

    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}"

if __name__ == "__main__":
    print(get_text_from_url("https://www.google.com/"))
    print(get_img_from_url("https://www.google.com/"))