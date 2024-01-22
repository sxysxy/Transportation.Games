import flask
import markdown2
import os
import argparse

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
    argps = argparse.ArgumentParser()
    argps.add_argument("--host", default="0.0.0.0", help="Default = 0.0.0.0, listen to all loop-back addresses.")
    argps.add_argument("--port", default=None, type=int, help="If product-env is false, port = 12345, otherwise port = 80 or 443(if enable-ssl)")
    argps.add_argument("--product-env", type=lambda x : x in ['y', 'Y'], default=False)  # 是否是生产环境，默认是开发&开发环境
    argps.add_argument("--enable-ssl", default=False, type=lambda x : x in ['y', 'Y'], help="If true, please specific ssl-cert and ssl-key")
    argps.add_argument("--ssl-cert", type=str, default=None, help="Path to SSL cert.pem")  # SSL证书文件
    argps.add_argument("--ssl-key", type=str, default=None, help="Path to SSL key.pem")    # SSL证书文件
    argps.add_argument("--sql-server", type=str, default="localhost:3306")
    argps.add_argument("--sql-engine", type=str, default=None)
    argps.add_argument("--sql-user", type=str, default=None)
    argps.add_argument("--sql-passwd", type=str, default=None)
    argps.add_argument("--sql-dbname", type=str, default="TransportationGame")
    
    args = argps.parse_args()
    
    if not all([args.sql_engine, args.sql_user, args.sql_passwd]):
        print("Warning: Missing SQL configuration, some function is disabled.")
    
    if args.port is None:
        if args.enable_ssl:
            args.port = 443
        else:
            args.port = 80
            
    if args.enable_ssl:
        if not all([args.ssl_cert, args.ssl_key]):
            print("[ABORTED] Error: --ssl-key or --ssl-cert is not set.")
            exit(1)
    
    if not args.product_env: 
    
        app.run(host=args.host,
                port=args.port, debug=True,
                ssl_context=(args.ssl_cert, args.ssl_key) if args.enable_ssl else None)   # 如果有SSL证书了可以整上去，没就算了
    
    else:
        http_prefix = "https" if args.enable_ssl else "http"
        if args.host == "0.0.0.0":
            print(f"Start server on {http_prefix}://localhost:{args.port}")
        else:
            print(f"Start server on {http_prefix}://{args.host}:{args.port}")
            
        print("------- Start WSGI Server -------")
        
        from gevent import pywsgi, monkey
        monkey.patch_all()
        
        if args.enable_ssl:
            server = pywsgi.WSGIServer((args.host, args.port), app, keyfile=args.ssl_key, certfile=args.ssl_cert)
        else:
            server = pywsgi.WSGIServer((args.host, args.port), app)
        server.serve_forever()
        
       
        