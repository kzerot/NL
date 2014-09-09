import tornado.ioloop
import tornado.web
import os
import json
import db

logins = {"admin": "admin"}


class App():
    class BaseHandler(tornado.web.RequestHandler):
        def get_current_user(self):
            self.db = db.DB()
            login = ''
            password = ''
            try:
                login = self.get_secure_cookie("login", None).decode('utf-8')
                password = \
                    self.get_secure_cookie("password", None).decode('utf-8')
                if login and password and logins[login] == password:
                    return login
                else:
                    return None
            except:
                return None

    class MainHandler(BaseHandler):
        @tornado.web.authenticated
        def get(self):
            self.render("index.html")

    class LoginHandler(BaseHandler):
        def get(self):
            self.render("login.html")

        def post(self):
            login = self.get_argument("login")
            password = self.get_argument("password")
            if logins[login] == password:
                self.set_secure_cookie("login", login)
                self.set_secure_cookie("password", password)
                self.redirect("/")
            else:
                self.redirect("/login")

    class ItemsHandler(BaseHandler):
        @tornado.web.authenticated
        def get(self):
            self.render("baseitems.html")

    class SkillsHandler(BaseHandler):
        @tornado.web.authenticated
        def get(self):
            self.render("skillsitems.html")

    class NpsHandler(BaseHandler):
        @tornado.web.authenticated
        def get(self):
            self.render("baseitems.html")

    class QuestHandler(BaseHandler):
        @tornado.web.authenticated
        def get(self):
            self.render("baseitems.html")

    class JsonHandler(BaseHandler):
        @tornado.web.authenticated
        def post(self):
            data = tornado.escape.json_decode(self.request.body)
            d = {}
            print("in", data)
            table = data['table']
            if "delete_prop" in data:
                if "itemId" in data and "node" in data:
                    self.db.deleteProp(data["itemId"], data["node"])
                    d = self.db.uniGet(data["itemId"], table)
            if "delete" in data:
                if "itemId" in data:
                    d = self.db.deleteItem(data["itemId"], table)
            elif "add" in data:
                if "name" in data:
                    itemId = None
                    if "itemId" in data:
                        itemId = data["itemId"]
                    d = self.db.addItem(itemId, data["name"], table)
                print(d)
            elif "save" in data:
                if "itemId" in data and "data" in data:
                    self.db.updateItem(data["itemId"], data["data"], table)
                    d = {'result': True}
            elif "id" in data:
                d = self.db.uniGetAllWeb(table)
            elif "itemId" in data:
                d = self.db.uniGet(data["itemId"], table)
            self.set_header("Content-Type", "application/json")
            self.content_type = 'application/json'

            self.write(d)

    def __init__(self):
        routes = [
            (r"/", self.MainHandler),
            (r"/getitems", self.JsonHandler),
            (r"/quests", self.QuestHandler),
            (r"/login", self.LoginHandler),
            (r"/items", self.ItemsHandler),
            (r"/skills", self.SkillsHandler),
            (r"/nps", self.NpsHandler),
            (r'/css/^(.*)', tornado.web.StaticFileHandler,
                {'path': '/css'},),
            (r'/templates/^(.*)', tornado.web.StaticFileHandler,
                {'path': '/templates'},),
            (r'/js/^(.*)', tornado.web.StaticFileHandler,
                {'path': '/js'},),
            (r'/plugins/^(.*)', tornado.web.StaticFileHandler,
                {'path': '/plugins'},),
        ]

        self.application = tornado.web.Application(
            routes,
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            cookie_secret="4qwet564d646343dsgxdfhsjm434",
            login_url="/login",
            debug=True,
        )
        #Database settings
        self.client = None
        self.db = None

    app = None

    @staticmethod
    def db():
        return App.instance().db

    @staticmethod
    def cp():
        return App.instance().cp

    @staticmethod
    def instance():
        if App.app is None:
            App.app = App()
        return App.app


app = App()
app.application.listen(8888)
tornado.ioloop.IOLoop.instance().start()
