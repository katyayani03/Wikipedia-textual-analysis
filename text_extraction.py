import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def text_ext():
    '''Purpose: Reads the input file and sends requests each url to extract data and then save the data to a file with the corresponding
        title as the file name.
    '''
    def extract_article(link):
        '''Purpose: This function retrieves the article from the given URL and extracts the body.
        Parameters: link – the link to which the request needs to be sent to extract text from.
        Returns: body – the body of the article
        '''
        response = requests.get(link)
        response.raise_for_status()
        data = response.text

        soup = BeautifulSoup(data, 'html.parser')

        # title = soup.find(class_="mw-page-title-main")
        # title = title.get_text() if title else 'No Title Found'
        
        body_paras = soup.select("#mw-content-text > div.mw-content-ltr.mw-parser-output > p")
        body = [b.get_text() if b else 'No Article Text Found' for b in body_paras]
        body = ' '.join(body)

        return body


    def save_article_to_file(article_title, body):
        '''Purpose: saves the extracted article (title and body) to a text file with the name as the corresponding title
        Parameters: article_title – the title of the article
	                body - the extracted body of the article (returned by the extract_title function)
  	    Returns None
        '''
        output_dir = 'articles'
        os.makedirs(output_dir, exist_ok=True)

        filename = os.path.join(output_dir, f"{article_title}.txt")

        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f"{article_title}\n\n")
                file.write(body)
        except FileNotFoundError:
            print(f"Error: File {filename} not found. Skipping this file.")


    def process_articles(input_f):
        '''Purpose: main function that reads the input Excel file, processes each article, and saves the results.
        Parameters: input_f – path to the Input.xsls file.
        Returns None
        '''
        df = pd.read_excel(input_f)
        for index, row in df.iterrows():
            article_title = row['Article_title']
            article_link = row['Article_link']

            body = extract_article(article_link)

            save_article_to_file(article_title, body)
            print(f"Saved article for {article_title} ({article_link})")


    input_f = 'Input.xlsx' #path of the input file
    process_articles(input_f)
