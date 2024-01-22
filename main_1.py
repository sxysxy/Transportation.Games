import flask
import markdown2
import os

import secrets
my_secret_key = secrets.token_urlsafe(16)


app = flask.Flask(__name__)
app.secret_key = my_secret_key


MAIN_PAGE_MARKDOWN_FILENAME = "./主页Markdown.md"
RANK_PAGE_MARKDOWN_FILENAME = "./排行榜Markdown.md"

class EasyFileCache:
    CACHES = {}
    
    def __init__(self, source, timestamp, content) -> None:
        self.source = source
        self.timestamp = timestamp
        self.content = content

# 判断是否是移动端设备(Android/ios)访问
def is_mobile():
    UA = str(flask.request.user_agent)
    return 'Android' in UA or 'iPhone' in UA

def validate_user(username, password):

    return username == "admin" and password == "password"
    
@app.route("/")
@app.route("/index")
def index():
    return flask.render_template("index.html")

@app.route("/upload")
def upload():
    if 'logged_in' in flask.session and flask.session['logged_in']:
        return flask.render_template("upload.html")
    else:
        # 如果用户未登录，返回一个包含登录页面的特殊HTML
        return flask.render_template("login.html")

    #return flask.render_template("upload.html")

@app.route("/rank")
def rank():
    return flask.render_template("rank.html")

@app.route('/login', methods=['GET', 'POST'])

def login():
    if flask.request.method == 'POST':

        username = flask.request.form['username']
        password = flask.request.form['password']
        if validate_user(username, password):
            flask.session['logged_in'] = True
            return flask.redirect(flask.url_for('upload'))
        else:
            return "用户名或密码错误", 401
        
    else:
        # 处理 GET 请求 - 显示登录页面
        return flask.render_template("login.html", is_mobile=is_mobile())
@app.route('/register', methods=['GET', 'POST'])
def register():
    username = flask.request.form['username']
    password = flask.request.form['password']
    email = flask.request.form['email']

    return flask.redirect(flask.url_for('login'))
# 主页
def get_markdown_content(filename):
    def loadf():
        with open(filename, "r",encoding="utf-8") as f:
            content = markdown2.markdown(f.read())
            
        obj = EasyFileCache(filename, int(os.path.getmtime(filename)), content)
        return obj
    
    if filename in EasyFileCache.CACHES:
        if int(os.path.getmtime(filename)) > EasyFileCache.CACHES[filename].timestamp:
            EasyFileCache.CACHES[filename] = loadf()
    else:
        EasyFileCache.CACHES[filename] = loadf()
    return EasyFileCache.CACHES[filename].content

@app.route("/markdown_of_main_page")
def markdown_of_main_page():
    return get_markdown_content(MAIN_PAGE_MARKDOWN_FILENAME)

@app.route("/markdown_of_rank_page")
def markdown_of_rank_page():
    return get_markdown_content(RANK_PAGE_MARKDOWN_FILENAME)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12345, debug=True)
