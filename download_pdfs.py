
import os
import requests
import json

# Load the PDF links from the JSON file
input_file = 'iso_ne_pdf_links.json'
output_folder = 'downloaded_pdfs'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the links
with open(input_file, 'r') as f:
    pdf_links_by_section = json.load(f)

# Download each PDF
for section, links in pdf_links_by_section.items():
    print(f"Downloading PDFs from section: {section}")
    for i, link in enumerate(links):
        try:
            # Ensure the link is absolute
            if not link.startswith('http'):
                link = 'https://www.iso-ne.com' + link

            # Generate a filename
            filename = os.path.join(output_folder, f"{section.split('/')[-1]}_{i+1}.pdf")

            # Download the PDF
            response = requests.get(link)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download {link}, status code: {response.status_code}")

        except Exception as e:
            print(f"Error downloading {link}: {str(e)}")

print("All PDFs have been downloaded to the folder:", output_folder)
