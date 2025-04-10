import pandas as pd
import requests
import random
from bs4 import BeautifulSoup
from datetime import date
import warnings
import re
from urllib.parse import urljoin

def get_all_ad_links(base_url):
    all_links = []
    ad_ids = set()  # Set to keep track of unique ad IDs
    page = 1

    while True:
        # Update the page query parameter
        url = f"{base_url}&Page={page}"
        print(f"Visiting page {page}...")

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch page {page}, status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        # Find all links with class 'Link_vis'
        ad_links = soup.find_all("a", class_="Link_vis")
        if not ad_links:  # Stop if no more links are found
            print("No more ads found. Stopping.")
            break

        if page == 5:
          break

        # Extract the href attribute from each link
        for ad_link in ad_links:
            href = ad_link.get("href")
            if href:
                absolute_url = urljoin("https://www.pazar3.mk", href)  # Convert to absolute URL
                if absolute_url not in ad_ids:  # Check if the link is unique
                    ad_ids.add(absolute_url)
                    all_links.append(absolute_url)  # Add the link to the list

        page += 1

    print(f"Found {len(all_links)} unique ad links.")
    return all_links

def scrape_page(url):
    obj = {}
    obj['Source'] = "pazar3"
    obj['Link'] = url
    obj['Id'] = url.split("/")[-1]  # Extract ID from URL (assuming it's the last part of the URL)

    response = requests.get(url)
    if response.status_code != 200:
        obj['Error'] = f"Failed to fetch page, status code: {response.status_code}"
        return obj

    raw_html = response.text
    html = BeautifulSoup(raw_html, "html.parser")

    # Extract Images
    images = []
    image_elements = html.find_all("a", class_="bootstrap4 custom-photo-link")
    for img_elem in image_elements:
        img_url = img_elem.get("href")
        if img_url:
            images.append(img_url)
    obj['Images'] = images

    # Extract Properties
    properties = {}
    property_elements = html.find_all("a", class_="tag-item")
    for prop_elem in property_elements:
        property_name = prop_elem.find("span").get_text(strip=True) if prop_elem.find("span") else None
        property_value = prop_elem.find("bdi").get_text(strip=True) if prop_elem.find("bdi") else None
        if property_name and property_value:
            properties[property_name] = property_value
    obj['Properties'] = properties

    # Extract Description
    description_elem = html.find("div", class_="description-area")
    obj['Description'] = description_elem.get_text(strip=True) if description_elem else None

    # Extract Phone Number
    phone_elem = html.find("a", href=lambda href: href and href.startswith("tel:"))
    obj['Phone'] = phone_elem.get("href").split(":")[1] if phone_elem else None

    # Extract User Name
    user_elem = html.find("div", class_="user-name ci-text-base")
    obj['User'] = user_elem.get_text(strip=True) if user_elem else None

    # Extract Date of Publish
    publish_date_elem = html.find("span", string="Објавени:")
    if publish_date_elem:
        date_base = publish_date_elem.find_next("span", class_="ci-text-base")
        time_bdi = date_base.find_next("bdi") if date_base else None
        obj['Publish Date'] = f"{date_base.get_text(strip=True)} {time_bdi.get_text(strip=True)}" if date_base and time_bdi else None
    else:
        obj['Publish Date'] = None

    return obj

def scrape_pazar3(**kwargs):
    search_url = "https://www.pazar3.mk/oglasi/zivealista/stanovi/skopje?"
    ad_links = get_all_ad_links(search_url)
    print(ad_links)

    ads = []

    for link in ad_links:
        try:
            ad = scrape_page(link)  # Attempt to scrape the page
            ads.append(ad)  # Append the scraped data to the list
        except Exception as e:
            print(f"Error while scraping {link}: {e}")  # Print an error message and skip the link
    kwargs['ti'].xcom_push(key='scraped_data', value=ads)