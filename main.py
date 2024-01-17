import flask

app = flask.Flask(__name__)

# 判断是否是移动端设备(Android/ios)访问
def is_mobile():
    UA = str(flask.request.user_agent)
    return 'Android' in UA or 'iPhone' in UA
    
# 主页
@app.route("/")
@app.route("/index")
def index():
    return flask.render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12345, debug=True)