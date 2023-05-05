import requests
from bs4 import BeautifulSoup
import json
import csv
import re
from scrapingbee import ScrapingBeeClient
from lxml import html
from dotenv import load_dotenv
import os

# take api key from .env file 
api_key = os.getenv('API_KEY')

def proxies(url):
    client = ScrapingBeeClient(api_key=api_key)

    response = client.get(url,
        params = { 
            'premium_proxy': 'True',
            'custom_google': 'True',
        }
    )
    return response


class Crawler:
    def __init__(self, query):
        self.query = query
        self.results_per_page = 10
        self.num_pages = 1000
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        self.result = []


    def get_num_results(self):
        # loop over the pages
        for i in range(self.num_pages):
            # calculate the start index for this page
            start_index = i * self.results_per_page

            # construct the URL of the search engine for this page
            url = f'https://www.google.com/search?q={self.query}&num={self.results_per_page}&start={start_index}'
            print(url)

            # send a GET request to the search engine using a proxy (optional)
            response = proxies(url)

            # parse the HTML content using BeautifulSoup
            tree = html.fromstring(response.content)

            # find all links on the page
            links = tree.xpath('//a[@href]')
            print(len(links))

            # loop over the links
            for link in links:
                link = link.get('href')
                
                # check if the link is a Google redirect link
                if link.startswith('/url?esrc=s&q=&rct=j&sa=U&url='):
                    # extract the target URL from the Google redirect link
                    link = link[30:]
                    
                    # check if the target URL is a YouTube link
                    if link.startswith('https://www.youtube.com/'):
                        # extract the channel URL and add it to the results
                        print(link)
                        link = link.split('&')[0]
                        self.result.append(link)
                else:
                    # check if the link is a YouTube link
                    if link.startswith('https://www.youtube.com/'):
                        # extract the channel URL and add it to the results
                        print(link)
                        link = link.split('&')[0]
                        self.result.append(link)

                
    def save_to_json(self):
        # This method saves the result to json
        with open('result.json', 'w') as f:
            json.dump(self.result, f, indent=4)

    def save_to_csv(self):
        with open('result.csv', 'w') as f:
            writer = csv.writer(f)

            # Write the header
            writer.writerow(['Channel link'])

            # Write each link
            for link in self.result:
                writer.writerow([link])

    def main(self):
        self.get_num_results()
        self.save_to_json()
        self.save_to_csv()


if __name__ == '__main__':
    crawler = Crawler('site:youtube.com openinapp.co')
    crawler.main()
