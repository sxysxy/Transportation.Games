# 后台页面，可以单独运行，甚至可以不需要和主页面在同一台机器上运行
import flask 
from common import get_args, App

class BackendApp(App):
    def __init__(self, args) -> None:
        if args.port is None:
            args.port = 12346
        super().__init__(args, template_folder="./backend_templates")

        if self.datamodel is None:
            raise RuntimeError("未能连接到SQL数据库，后台管理程序无法运行")
            
        self.app.add_url_rule("/", view_func=self.backend)
        self.app.add_url_rule("/backend", view_func=self.backend)
        
    def backend(self):
        return flask.render_template("backend.html", 
                                     stat_view_main=self.datamodel.backend_stat_int_get('view_main'),
                                     stat_view_rank=self.datamodel.backend_stat_int_get('view_rank')
                                     )

if __name__ == "__main__":
    BackendApp(get_args()).run()