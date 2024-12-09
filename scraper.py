
import os
import requests
import json
from urllib.parse import urljoin, unquote
from pathlib import Path
import time
from tqdm import tqdm

def sanitize_filename(filename):
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def download_pdf(url, output_folder, section_name):
    try:
        # Ensure the URL is absolute
        if not url.startswith('http'):
            url = urljoin('https://www.iso-ne.com', url)
        
        # Extract filename from URL
        filename = unquote(url.split('/')[-1])
        filename = sanitize_filename(filename)
        
        # Create section subfolder
        section_folder = os.path.join(output_folder, sanitize_filename(section_name))
        os.makedirs(section_folder, exist_ok=True)
        
        # Full path for the file
        filepath = os.path.join(section_folder, filename)
        
        # Don't download if file already exists
        if os.path.exists(filepath):
            return True, f"File already exists: {filepath}"
        
        # Download with timeout and retries
        for attempt in range(3):
            try:
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    return True, filepath
                else:
                    time.sleep(1)  # Wait before retry
            except requests.RequestException:
                if attempt < 2:  # Don't sleep on last attempt
                    time.sleep(2)
        
        return False, f"Failed to download after 3 attempts: {url}"
    
    except Exception as e:
        return False, f"Error downloading {url}: {str(e)}"

def main():
    # Load the PDF links
    with open('consolidated_iso_ne_pdf_links.json', 'r') as f:
        pdf_links = json.load(f)
    
    # Create main output folder
    output_folder = 'iso_ne_pdfs'
    os.makedirs(output_folder, exist_ok=True)
    
    # Count total PDFs
    total_pdfs = sum(len(links) for links in pdf_links.values())
    
    print(f"Starting download of {total_pdfs} PDFs...")
    
    # Track success and failures
    successful = []
    failed = []
    
    # Process each section
    with tqdm(total=total_pdfs, desc="Downloading PDFs") as pbar:
        for section_url, links in pdf_links.items():
            # Get section name from URL
            section_name = section_url.split('/')[-1]
            
            # Process each PDF in the section
            for link in links:
                success, message = download_pdf(link, output_folder, section_name)
                if success:
                    successful.append(message)
                else:
                    failed.append(message)
                pbar.update(1)
    
    # Save download report
    report = {
        'total_pdfs': total_pdfs,
        'successful_downloads': len(successful),
        'failed_downloads': len(failed),
        'failed_urls': failed
    }
    
    with open(os.path.join(output_folder, 'download_report.json'), 'w') as f:
        json.dump(report, f, indent=4)
    
    print(f"\nDownload completed!")
    print(f"Successfully downloaded: {len(successful)} PDFs")
    print(f"Failed downloads: {len(failed)} PDFs")
    print(f"\nDetailed report saved to: {os.path.join(output_folder, 'download_report.json')}")
    print(f"PDFs are organized by section in: {output_folder}/")

if __name__ == "__main__":
    main()
