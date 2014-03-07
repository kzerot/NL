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
            print("REQUEST", self.request)
            print("CONTENT", self.request.body)
            data = tornado.escape.json_decode(self.request.body)
            d = {}
            if("id" in data):
                d = self.db.getItemsAllWeb()
                print (d)
            elif "itemId" in data:
                d = self.db.getItem(data["itemId"])
                print (d)
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
