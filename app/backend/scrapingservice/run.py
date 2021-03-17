import tornado.ioloop
import tornado.web
import json
import asyncio
import requests

from scraper import RedditScraper
from config import SCRAPING_SERVICE_PORT,DB_SERVICE_IP,DB_SERVICE_PORT

db_url =f'http://{DB_SERVICE_IP}:{DB_SERVICE_PORT}/api/v1/store'

class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Content-Type', 'application/json')



    def get(self,country):
        #get the data from the scraper
        res = RedditScraper().top_3_from_country(country)
        #store in db
        requests.post(url=db_url,json={"id": country, "posts":res})
        #return the results
        self.write(json.dumps(res))

def make_app():
    return tornado.web.Application([
        (r"/api/v1/reddit-top-3/([^/]+)?", MainHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(SCRAPING_SERVICE_PORT)
    tornado.ioloop.IOLoop.current().start()

    # http://localhost:8888/api/v1/top3/United%20States