Running the Menu Scraper Script

This Python script allows you to scrape menu items from a restaurant's Zomato page and store them in a SQLite database.

Prerequisites

Before running the script, ensure you have the following installed:

Python 3.x
pip (Python package manager)

Installation

1. Clone or download this repository to your local machine.

2. Install the required Python packages by running the following command in your terminal:

    pip install -r requirements.txt

3. Ensure you have Tesseract OCR installed on your machine. You can download it from [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract) and follow the installation instructions for your operating system.

Usage

1. Run the script by executing the following command in your terminal:

    python menu_scraper.py

2. Give/Paste Zomato Restaurant URL like: https://www.zomato.com/mumbai/zam-zam-cateres-family-restaurant-kurla

3. The script will fetch the menu images from the Zomato page, perform OCR (Optical Character Recognition) to extract text from the images, parse the menu items, and store them in a SQLite database named `menus.db`.

4. After running the script, you can check the `menus.db` file to view the stored menu items.

Notes

Ensure you have an internet connection while running the script to fetch the menu images from Zomato.
Make sure the Tesseract OCR executable path (`pytesseract.pytesseract.tesseract_cmd`) is correctly set in the script.
