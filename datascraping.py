import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import fitz  # PyMuPDF

# URL of the main webpage with subsections
base_url = "https://www.iso-ne.com/participate/rules-procedures"

# Path to save downloaded PDFs and extracted text files
save_path = r"C:\Users\ishit\Downloads\320 iso"

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
            
            # Write the content to a PDF file
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}")

            # Extract text to a .txt file
            extract_text_from_pdf(file_path, save_path)

        else:
            print(f"Failed to download: {pdf_url}")
    except Exception as e:
        print(f"Error downloading {pdf_url}: {e}")

# Function to extract text from a PDF and save it as a .txt file
def extract_text_from_pdf(pdf_path, save_path):
    try:
        # Open the PDF file
        with fitz.open(pdf_path) as pdf:
            # Define the text file path
            text_file_name = os.path.splitext(os.path.basename(pdf_path))[0] + ".txt"
            text_file_path = os.path.join(save_path, text_file_name)

            # Extract text from each page
            with open(text_file_path, "w", encoding="utf-8") as text_file:
                for page_num in range(pdf.page_count):
                    page = pdf[page_num]
                    text = page.get_text()
                    text_file.write(text)

            print(f"Extracted text saved to: {text_file_name}")
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")

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
                
                # Download the PDF and extract its text
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

    print("All PDFs downloaded and text extracted.")
else:
    print(f"Failed to retrieve the main webpage. Status code: {response.status_code}")
