import flask
import markdown2
import os
from datamodel import DataModel
import json
from common import get_args, App
import time

MAIN_PAGE_MARKDOWN_FILENAME = "./主页Markdown.md"
RANK_PAGE_MARKDOWN_FILENAME = "./排行榜Markdown.md"

class EasyFileCache:
    CACHES = {}
    
    def __init__(self, source, timestamp, content) -> None:
        self.source = source
        self.timestamp = timestamp
        self.content = content
        
class FrontendApp(App):
    def __init__(self, args) -> None:
        super().__init__(args)
        if self.datamodel is None:
            print("Warning: Missing SQL configuration, some function is disabled.")
            print(f"SQL Exception:\n{self.sql_exception}")
        self._icp_license = args.icp_license
        
        self.app.add_url_rule("/", view_func=self.index)
        self.app.add_url_rule("/index", view_func=self.index)
        self.app.add_url_rule("/footer", view_func=self.footer)
        self.app.add_url_rule("/markdown_of_main_page", view_func=self.markdown_of_main_page)
        self.app.add_url_rule("/rank", view_func=self.rank)
        self.app.add_url_rule("/markdown_of_rank_page", view_func=self.markdown_of_rank_page)
        self.app.add_url_rule("/nosqlerror", view_func=self.nosqlerror)
        self.app.add_url_rule("/upload", view_func=self.upload)
        self.app.add_url_rule("/login", view_func=self.login, methods=['GET', 'POST'])
        self.app.add_url_rule("/register", view_func=self.register)
        self.app.add_url_rule("/get_main_stat", view_func=self.get_main_stat)
        self.app.add_url_rule("/get_rank_stat", view_func=self.get_rank_stat)
        
        self.app.add_url_rule("/icp_license", view_func=self.icp_license)
        
    @staticmethod
    def is_mobile():
        UA = str(flask.request.user_agent)
        return 'Android' in UA or 'iPhone' in UA
    
    def icp_license(self):
        return str(self._icp_license)

    def index(self):
        if self.datamodel:
            self.datamodel.backend_stat_int_add("view_main", 1)
        return flask.render_template("index.html", is_mobile=self.is_mobile())
    
    def rank(self):
        if self.datamodel:
            self.datamodel.backend_stat_int_add("view_rank", 1)
        return flask.render_template("rank.html", is_mobile=self.is_mobile())
    
    def footer(self):
        return flask.render_template("footer.html")
    
    def get_page_stat(self, var_name, filename):
        dt = time.localtime(os.path.getmtime(filename))
        if self.datamodel:
            n = self.datamodel.backend_stat_int_get(var_name)
        else:
            n = 0
        return json.dumps({
            "num" : n,
            "mtime" : time.strftime("最后更新时间: %Y年%m月%d日 %H:%M:%S", dt)
        })
        
    def get_main_stat(self):
        return self.get_page_stat("view_main", MAIN_PAGE_MARKDOWN_FILENAME)
    
    def get_rank_stat(self):
        return self.get_page_stat("view_rank", RANK_PAGE_MARKDOWN_FILENAME)
            
    def upload(self):
        return flask.render_template("/building.html", is_mobile=self.is_mobile)
        # if 'logged_in' in flask.session and flask.session['logged_in']:
        #     return flask.render_template("upload.html")
        # else:
        #     return flask.render_template("login.html")
        
    # 美化Makrdown样式
    makrdown_css = '''
    table {
        border : 1px solid black;   
    }
    '''
    def render_makrdown(self, markdown_source):
        html = markdown2.markdown(markdown_source, extras=['tables'])
        # soup = BeautifulSoup(html, 'html.parser')
        # style_tag = soup.new_tag('style', 'text/css')
        # style_tag.string = self.makrdown_css
        # soup.append(style_tag)
        # return str(soup)
        return html
        
    def get_markdown_content(self, filename):
        def loadf():
            with open(filename, "r",encoding="utf-8") as f:
                content = self.render_makrdown(f.read())
                
            obj = EasyFileCache(filename, int(os.path.getmtime(filename)), content)
            return obj
        
        if filename in EasyFileCache.CACHES:
            if int(os.path.getmtime(filename)) > EasyFileCache.CACHES[filename].timestamp:
                EasyFileCache.CACHES[filename] = loadf()
        else:
            EasyFileCache.CACHES[filename] = loadf()
        return EasyFileCache.CACHES[filename].content

    def markdown_of_main_page(self):
        return self.get_markdown_content(MAIN_PAGE_MARKDOWN_FILENAME)

    def markdown_of_rank_page(self):
        return self.get_markdown_content(RANK_PAGE_MARKDOWN_FILENAME)

    def nosqlerror(self):
        return flask.render_template("nosqlerror.html")

    def login(self):
        if not self.datamodel:
            return flask.redirect(flask.url_for('nosqlerror'))
        
        if flask.request.method == 'POST':

            username = flask.request.form['username']
            password = flask.request.form['password']
            if self.datamodel.loginuser(username, password):
                flask.session['logged_in'] = True
                return flask.redirect(flask.url_for('upload'))
            else:
                return "用户名或密码错误", 401
            
        else:
            # 处理 GET 请求 - 显示登录页面
            return flask.render_template("login.html", is_mobile=self.is_mobile())
        
    def register(self):
        username = flask.request.form['username']
        password = flask.request.form['password']
        password2 = flask.request.form['password_confirm']
        email = flask.request.form['email']
        self.datamodel.registeruser(username, password, password2, email)
        return flask.redirect(flask.url_for('login'))


if __name__ == "__main__":
    FrontendApp(get_args()).run()
        
       
        