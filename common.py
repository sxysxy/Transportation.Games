import argparse
from datamodel import DataModel
import flask
import secrets

def get_args():
    argps = argparse.ArgumentParser()
    argps.add_argument("--host", default="0.0.0.0", help="Default = 0.0.0.0, listen to all loop-back addresses.")
    argps.add_argument("--port", default=None, type=int, help="If product-env is false, port = 12345, otherwise port = 80 or 443(if enable-ssl)")
    argps.add_argument("--product-env", type=lambda x : x in ['y', 'Y'], default=False)  # 是否是生产环境，默认是开发&开发环境
    argps.add_argument("--enable-ssl", default=False, type=lambda x : x in ['y', 'Y'], help="If true, please specific ssl-cert and ssl-key")
    argps.add_argument("--ssl-cert", type=str, default=None, help="Path to SSL cert.pem")  # SSL证书文件
    argps.add_argument("--ssl-key", type=str, default=None, help="Path to SSL key.pem")    # SSL证书文件
    argps.add_argument("--sql-server", type=str, default="localhost:3306")
    argps.add_argument("--sql-engine", type=str, default="mysql+pymysql")
    argps.add_argument("--sql-user", type=str, default=None)
    argps.add_argument("--sql-passwd", type=str, default=None)
    argps.add_argument("--sql-dbname", type=str, default="TransportationGames")
    argps.add_argument("--icp-license", type=str, default=None)
    argps.add_argument("--forward-http2https", type=lambda x : x in ['y', 'Y'], default=False, help="Whether to forward http to https(valid when --enbale-ssl is enabled)")
    argps.add_argument("--forward-http-port", type=int, default=80)
    return argps.parse_args()

class App:
    def __init__(self, args, **flask_options) -> None:
        app = flask.Flask("__main__", **flask_options)
       
        if not args.sql_passwd:
            args.sql_passwd = ""
        
        if args.port is None:
            if args.product_env:
                if args.enable_ssl:
                    args.port = 443
                else:
                    args.port = 80
            else:
                args.port = 12345
                
        if args.enable_ssl:
            if not all([args.ssl_cert, args.ssl_key]):
                print("[ABORTED] Error: --ssl-key or --ssl-cert is not set.")
                exit(1)
                
        if args.sql_user:
            try:
                self.datamodel = DataModel(args.sql_engine, args.sql_server, args.sql_user, args.sql_passwd, args.sql_dbname)
                self.sql_exception = None
            except Exception as e:
                self.datamodel = None
                self.sql_exception = e
        else:
            self.datamodel = None
        
        if not args.product_env: 
        
            def runner():
                app.run(host=args.host,
                        port=args.port, debug=True,
                        ssl_context=(args.ssl_cert, args.ssl_key) if args.enable_ssl else None)   # 如果有SSL证书了可以整上去，没就算了
        
        else:
            http_prefix = "https" if args.enable_ssl else "http"
            if args.host == "0.0.0.0":
                print(f"Start server on {http_prefix}://localhost:{args.port}")
            else:
                print(f"Start server on {http_prefix}://{args.host}:{args.port}")
                
            def runner():
                print("------- Start WSGI Server -------")
                
                from gevent import pywsgi, monkey
                monkey.patch_all()
                
                if args.enable_ssl:
                    server = pywsgi.WSGIServer((args.host, args.port), app, keyfile=args.ssl_key, certfile=args.ssl_cert)
                else:
                    server = pywsgi.WSGIServer((args.host, args.port), app)
                server.serve_forever()
                
        self.app = app
        self.runner = runner
        
    def run(self):
        return self.runner()
