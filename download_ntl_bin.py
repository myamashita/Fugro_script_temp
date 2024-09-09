import os
import requests
from bs4 import BeautifulSoup

# Base URL for the data
base_url = "https://ntl.gcoos.org/data/raw/42373/"
# Years to download
years = ["2022", "2023", "2024"]
# Create a directory to save the files
os.makedirs("data", exist_ok=True)

def download_files_from_url(url, save_dir):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href.endswith('/'):
                # If the link is a directory, recursively download files from the subdirectory
                new_dir = os.path.join(save_dir, href)
                os.makedirs(new_dir, exist_ok=True)
                download_files_from_url(url + href, new_dir)
            elif href.endswith('.bin'):
                file_url = url + href
                file_name = href.split('/')[-1]
                print(f"Downloading {file_name} from {file_url}")
                file_response = requests.get(file_url)
                if file_response.status_code == 200:
                    file_path = os.path.join(save_dir, file_name)
                    with open(file_path, 'wb') as f:
                        f.write(file_response.content)
                else:
                    print(f"Failed to download {file_name}")
    else:
        print(f"Failed to access {url}")

for year in years:
    year_url = f"{base_url}{year}/"
    download_files_from_url(year_url, os.path.join("data", year))
