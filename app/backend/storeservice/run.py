import tornado.web
import json
from store import FakeDB
from config import DB_SERVICE_PORT

#our in memo db instance
DB = FakeDB()

class FilterOptions :
    COUNTRY="country"
    TEXTUAL="textual"
    RATING="rating"


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({"posts":DB.get_all()})

    def post(self):
        if not self.request.body:
            return self.write({"message":"Error: body is empty"})

        data = json.loads(self.request.body)
        try:
            id = data["id"]
            post_list = data["posts"]
            DB.add(id=id,list_obj=post_list)
            return self.write({"message":"added successfully"})
        except Exception as e:
            print(e)
            return self.write({"message":"Error: missing some require data"})

class Filters(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Content-Type', 'application/json')

    def post(self,filter_by):
        if not self.request.body:
            return self.write({"message": "Error: body is empty"})

        data = json.loads(self.request.body)
        search_content = data["search_content"]

        if search_content == '':
            return self.write([])

        if filter_by == FilterOptions.COUNTRY:
            return self.write(json.dumps(DB.get_by_id(search_content)))

        if filter_by == FilterOptions.TEXTUAL:
            return self.write(json.dumps(DB.search_in_field(search_content,'title')))

        if filter_by == FilterOptions.RATING:
            return self.write(json.dumps(DB.search_in_field(search_content,'votes')))

        return self.write({"message":"filter option is not allowed."})

def make_app():
    return tornado.web.Application([
        (f"/api/v1/store", MainHandler),
        (f"/api/v1/store/filter/([^/]+)",Filters)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(DB_SERVICE_PORT)
    tornado.ioloop.IOLoop.current().start()