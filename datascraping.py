import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the main webpage with subsections
base_url = "https://www.iso-ne.com/participate/rules-procedures"

# Path to save downloaded PDFs
save_path = r"C:\Users\Srikiran\OneDrive\Documents\CS 320\ISO Website"

# Create the directory if it doesn't exist
if not os.path.exists(save_path):
    os.makedirs(save_path)

# Function to download a PDF
def download_pdf(pdf_url, save_path):
    try:
        response = requests.get(pdf_url)
        if response.status_code == 200:
            # Extract the file name from the URL
            file_name = pdf_url.split("/")[-1]
            file_path = os.path.join(save_path, file_name)
            
            # Write the content to a file
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to download: {pdf_url}")
    except Exception as e:
        print(f"Error downloading {pdf_url}: {e}")

# Function to scrape all PDFs from a given subsection URL
def scrape_pdfs_from_url(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all links that contain '.pdf'
        pdf_links = soup.find_all('a', href=True)
        
        for link in pdf_links:
            href = link['href']
            if href.endswith('.pdf'):
                # Make the full URL if the link is relative
                pdf_url = urljoin(url, href)
                
                # Download the PDF
                download_pdf(pdf_url, save_path)
    else:
        print(f"Failed to retrieve the webpage: {url}. Status code: {response.status_code}")

# Step 1: Request the main page to find subsection links
response = requests.get(base_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Step 2: Find all subsection links under the main page
    # Assuming subsection links are in 'div' with class 'section' or similar
    subsections = soup.find_all('a', href=True)
    
    for link in subsections:
        href = link['href']
        
        # Check if the link is valid and points to a subsection
        if href.startswith('/participate/rules-procedures/'):
            subsection_url = urljoin(base_url, href)
            print(f"Scraping PDFs from subsection: {subsection_url}")
            
            # Step 3: Scrape PDFs from each subsection
            scrape_pdfs_from_url(subsection_url, save_path)

    print("All PDFs downloaded.")
else:
    print(f"Failed to retrieve the main webpage. Status code: {response.status_code}")