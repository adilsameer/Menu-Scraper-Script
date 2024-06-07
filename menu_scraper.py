import requests
import sqlite3
import pytesseract
from PIL import Image
import os
from io import BytesIO
import re
from bs4 import BeautifulSoup

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_menu_images(restaurant_id):
    url = f"https://www.zomato.com/webroutes/menu/viewMenu?res_id={restaurant_id}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code != 200:
        print(f"Failed to fetch menu images: Status code {response.status_code}")
        return []

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")
        print("Response content:", response.text)
        return []

    menu_images = []
    sections = data.get("page_data", {}).get("sections", {})
    image_sections = sections.get("SECTION_IMAGE_MENU", {}).get("menuItems", [])

    for section in image_sections:
        for page in section.get("pages", []):
            menu_images.append(page["url"])

    return menu_images

def download_image(url, image_path):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    img = Image.open(BytesIO(response.content))
    img.save(image_path)

def perform_ocr(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

def parse_menu(text):
    menu_items = []
    sections = re.split(r'\n\n+', text)  # Split text by double newlines to identify sections

    for section in sections:
        lines = section.strip().split('\n')
        section_name = lines[0]  # First line is assumed to be the section name

        for line in lines[1:]:
            items = re.findall(r'(\D+)\s+(\d+)', line)  # Extract item and price using regex
            for item, price in items:
                menu_items.append((item.strip(), price.strip()))  # Append item and price as tuple

    return menu_items

def store_in_database(menu_items, db_name='menus.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS menu
                      (item TEXT, price TEXT)''')

    cursor.executemany('INSERT INTO menu (item, price) VALUES (?, ?)', menu_items)

    conn.commit()
    conn.close()

def cleanup_menu_directory():
    if os.path.exists('menu_images'):
        for file in os.listdir('menu_images'):
            file_path = os.path.join('menu_images', file)
            os.remove(file_path)
        os.rmdir('menu_images')

def main(restaurant_id):
    image_urls = get_menu_images(restaurant_id)

    if not os.path.exists('menu_images'):
        os.makedirs('menu_images')

    all_menu_items = []

    for i, url in enumerate(image_urls):
        image_path = f'menu_images/menu_{restaurant_id}_{i}.jpg'
        download_image(url, image_path)
        text = perform_ocr(image_path)
        menu_items = parse_menu(text)
        all_menu_items.extend(menu_items)
        os.remove(image_path)

    store_in_database(all_menu_items)
    print(f"Menu items for restaurant {input_url} have been stored in the database successfully.")
    cleanup_menu_directory()


if __name__ == "__main__":
    input_url = input("Give Zomato Restaurant Url(Ex:https://www.zomato.com/mumbai/zam-zam-cateres-family-restaurant-kurla):\n")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(input_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_links = [link for link in soup.find_all('a') if link.string == "Add a Zomato spoonback to your blog."]
    for link in all_links:
        if "spoonbacks" in link.get('href', ''):
            url = f"{link.get('href')}"
            parts = url.split('/')
            restaurant_id = parts[-1]
            main(restaurant_id)
            break
    else:
        print("Restaurant Id not found from given link")
