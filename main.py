import flask
import markdown2
import os

app = flask.Flask(__name__)
MAIN_PAGE_MARKDOWN_FILENAME = "./主页Markdown.md"

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
    
# 主页
@app.route("/")
@app.route("/index")
def index():
    return flask.render_template("index.html")


def get_markdown_content():
    def loadf():
        with open(MAIN_PAGE_MARKDOWN_FILENAME, "r") as f:
            content = markdown2.markdown(f.read())
            
        obj = EasyFileCache(MAIN_PAGE_MARKDOWN_FILENAME, int(os.path.getmtime(MAIN_PAGE_MARKDOWN_FILENAME)), content)
        return obj
    
    if 'markdown_of_main_page' in EasyFileCache.CACHES:
        if int(os.path.getmtime(MAIN_PAGE_MARKDOWN_FILENAME)) > EasyFileCache.CACHES['markdown_of_main_page'].timestamp:
            EasyFileCache.CACHES['markdown_of_main_page'] = loadf()
    else:
        EasyFileCache.CACHES['markdown_of_main_page'] = loadf()
    return EasyFileCache.CACHES['markdown_of_main_page'].content
        

@app.route("/markdown_of_main_page")
def markdown_of_main_page():
    return get_markdown_content()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12345, debug=True)