import pandas as pd
import requests
import random
from bs4 import BeautifulSoup
from datetime import date
import warnings
import re
from urllib.parse import urlparse, parse_qs

def get_ad_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    ad_id = query_params.get("ad", [None])[0]
    return ad_id

def scrape_page(url):

    headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Accept-Language': 'mk-MK,mk;q=0.9'
    }

    obj = {}
    obj['Source'] = "reklama5"
    obj['Link'] = url
    obj['Id'] = get_ad_id(url)

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        obj['Error'] = f"Failed to fetch page, status code: {response.status_code}"
        return obj

    raw_html = response.text
    html = BeautifulSoup(raw_html, "html.parser")

    # Extract properties
    properties = {}
    static_elements = html.find_all("div", class_="itemStatic")
    for static_element in static_elements:
        key = static_element.text.strip()
        value_element = static_element.find_next("div", class_="itemDinamic")
        value = value_element.text.strip() if value_element else None
        properties[key] = value
    obj['Properties'] = properties

    # Extract description
    description_element = html.find("p", class_="oglasDescription")
    obj['Description'] = description_element.text.strip() if description_element else "No description available"

    # Extract images
    images = []
    owl_carousel = html.find('div', class_='owl-carousel')
    if owl_carousel:
        img_tags = owl_carousel.find_all('img', class_='img-responsive')
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url:
                full_url = 'https:' + img_url if img_url.startswith('//') else img_url
                images.append(full_url)
    obj['Images'] = images

    # Extract user name
    user_name_element = html.find("b", class_="adValue-mobile user-name")
    if user_name_element:
        obj['User Name'] = user_name_element.text.strip()
    else:
        obj['User Name'] = "No user name available"

    # Extract phone number
    phone_element = html.find("a", class_="adValue-mobile", href=lambda href: href and href.startswith("tel:"))
    if phone_element:
        obj['Phone Number'] = phone_element.text.strip()
    else:
        obj['Phone Number'] = "No phone number available"

    # Extract location
    location_element = html.find("div", class_="place")
    if location_element:
        # Clean up text to remove extra spaces and slashes
        location_text = ' '.join(location_element.text.split()).replace(" / ", ", ")
        obj['Location'] = location_text
    else:
        obj['Location'] = "No location available"

    # Extract published date
    label_elements = html.find_all("label")
    for label in label_elements:
        if "Published on:" in label.text:
            published_date = label.text.replace("Published on:", "").strip()
            obj['Published Date'] = published_date
            break
    else:
        obj['Published Date'] = "No published date available"

    return obj

def get_all_ad_links(base_url):

    headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Accept-Language': 'mk-MK,mk;q=0.9'
    }
    
    all_links = []
    ad_ids = set()  # Set to keep track of unique ad IDs
    page = 1

    while True:
        # Update the page query parameter
        url = f"{base_url}&page={page}"
        print(f"Visiting page {page}...")

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page {page}, status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        # Find all links matching the AdDetails pattern
        ad_links = soup.find_all("a", href=re.compile(r"AdDetails\?ad=\d+"))
        if not ad_links:  # Stop if no more links are found
            print("No more ads found. Stopping.")
            break

        if page == 5:
          break

        # Extract the href attribute from each ad link
        for ad_link in ad_links:
            href = ad_link.get("href")
            if href:
                ad_id = re.search(r"AdDetails\?ad=(\d+)", href)
                if ad_id:
                    ad_id = ad_id.group(1)
                    if ad_id not in ad_ids:  # Check if the ad ID is not in the set
                        ad_ids.add(ad_id)  # Add the ad ID to the set
                        all_links.append(f"https://reklama5.mk/{href}")  # Add the full URL to the list

        page += 1

    print(f"Found {len(all_links)} unique ad links.")
    return all_links

def scrape_reklama5(**kwargs):
    search_url = "https://reklama5.mk/Search?city=267%2c268%2c270&cat=159&q=&f45_from=&f45_to=&f46_from=&f46_to=&priceFrom=&priceTo=&f48_from=&f48_to=&f47=&f10029=&f10030=&f10040=&sell=0&sell=1&buy=0&buy=1&rent=0&rent=1&includeforrent=0&includeforrent=1&trade=0&trade=1&includeOld=0&includeOld=1&includeNew=0&includeNew=1&cargoReady=0&DDVIncluded=0&private=0&company=0&SortByPrice=0&zz=1"
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