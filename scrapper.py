from bs4 import BeautifulSoup
import requests
import fitz  # PyMuPDF

class data_scrapper:
    def __init__(self):
        self.myWebData = []  # this stores the web data
        self.myPdfData = []  # this stores the pdf data
    
    def scrape_web_content(self, url:str):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove following tags
        # for tag in soup(['header', 'nav', 'footer']):
        #     tag.decompose()

        # Find all heading, paragraph, table, and list tags
        tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'table', 'ul', 'ol'])

        # Extract the text from each tag and remove leading/trailing whitespace
        self.myWebdata = []
        for tag in tags:
            self.myWebData += (tag.get_text()).split()
    

    def extract_pdf_content(self, pdf_content):
        try:
            myData = []
            with fitz.open(pdf_content) as pdf_document:
                num_pages = pdf_document.page_count
                for page_num in range(num_pages):
                    page = pdf_document[page_num]
                    text = page.get_text()
                    myData += text.split()
            if len(myData) > 0:
                self.myPdfData = myData
        except Exception as e:
            print(f"Error: {e}")