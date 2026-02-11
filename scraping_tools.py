import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from image_uploader import *


def get_text_from_url(url, timeout=10):  # ✅ Added timeout parameter
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator="\n", strip=True)
        linksChecked = 0
        print(f"📄 Scraping: {url[:60]}...")  # Better than "check1"

        '''
        for a in soup.find_all('a'):
            if linksChecked <= 5:
                href = a.get("href")
                if href:
                    try:
                        response = requests.get(
                            urljoin(url, href),
                            headers={'User-Agent': 'Mozilla/5.0'},
                            timeout=timeout  # ✅ Timeout on linked pages too
                        )
                        response.raise_for_status()
                        soup = BeautifulSoup(response.text, 'html.parser')
                        text += soup.get_text(separator="\n", strip=True)
                        linksChecked += 1
                    except (requests.exceptions.RequestException, Exception):
                        # Skip problematic linked pages silently
                        continue
                        
        '''

        return text
    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}"

def get_img_from_url(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')

        valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
        fallback_img = None

        for img in images:
            src = img.get('src')
            if not src:
                continue

            full_url = urljoin(url, src)

            if full_url.lower().endswith(valid_extensions):
                return full_url  # Found usable image
            elif not fallback_img:
                fallback_img = full_url  # Save first fallback

        # No usable image found; try uploading fallback to ImgBB
        if fallback_img:
            return upload_to_imgbb(fallback_img)

        return "No usable image found and no fallback available."

    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}"

def get_links_from_url(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        links = []

        for a in soup.find_all('a'):
            if not a.has_attr('href'):
                continue

            if 'http' not in a.get('href'):
                continue

            links.append(a.get('href'))

        return links
    except requests.exceptions.RequestException as e:
        return ""

if __name__ == "__main__":
    #print(get_text_from_url("https://www.google.com/"))
    #print(get_img_from_url("https://www.google.com/"))

    test_url = "https://www.bing.com/search?pglt=43&q=volunteer+oppurtunies&cvid=7e0fee03d18e4e168a956f8ccbc14fcd&gs_lcrp=EgRlZGdlKgYIABBFGDkyBggAEEUYOTIGCAEQABhAMgYIAhAAGEAyBggDEAAYQDIGCAQQABhAMgYIBRAAGEAyBggGEAAYQDIGCAcQABhAMgYICBAAGEAyCAgJEOkHGPxV0gEINTIyOGowajGoAgiwAgE&FORM=ANNAB1&DAF0=1&PC=U531"
    print(get_links_from_url(test_url))