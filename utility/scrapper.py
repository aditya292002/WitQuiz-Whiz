from bs4 import BeautifulSoup
import requests
import fitz  # PyMuPDF



def scrape_web_content(url:str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    content = []

    # Find all heading, paragraph, table, and list tags
    tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'table', 'ul', 'ol'])

    # Extract the text from each tag and remove leading/trailing whitespace
    for tag in tags:
        content += (tag.get_text()).split()
    return content

def extract_pdf_content(pdf_content):
    try:
        myData = []
        with fitz.open(pdf_content) as pdf_document:
            num_pages = pdf_document.page_count
            for page_num in range(num_pages):
                page = pdf_document[page_num]
                text = page.get_text()
                myData += text.split()
        if len(myData) > 0:
            return myData
    except Exception as e:
        print(f"Error: {e}")