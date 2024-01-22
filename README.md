# Transportation.Games
Source code of transportation.games(website) for paper <a href="https://arxiv.org/abs/2401.04471">TransportationGames: Benchmarking Transportation Knowledge of Multimodal Large Language Models</a>

# Setup 

```
git clone git@github.com:sxysxy/Transportation.Games.git 
```

or 

```
git clone https://github.com/sxysxy/Transportation.Games.git
```

then

```
conda activate your_virtual_env
pip install -r requirements.txt
```

# Run

### SQL数据库准备

（待完善）

### 服务端程序运行

For developing environment:

```
python main.py
```

The default port is 12345

For productive environment:

```
python main.py --product-env y
```

This will enable gevent.monkey.patch_all() and use a WSGIServer to run the flask app, the default port is 80 or 443(if SSL/TLS is enabled)


# 内容定制

为主页添加文本内容：在主页Markdown.md里直接编辑  
为排行榜添加文本内容：在排行榜Markdown.md里直接编辑

# 程序命令行参数

<table border=1, style="width:100%">
<thead>
<tr><td><b>参数</b></td> <td><b>含义</b></td> <td><b>默认值</b></td></tr>
</thead>
<tbody>
<tr><td>--host</td><td>服务程序监听的地址，默认监听本机所有回环地址。</td><td>0.0.0.0</td></tr>
<tr><td>--port</td><td>服务程序监听的端口，在开发调试环境下默认为12345，生产环境下默认80或443(依据是否开启SSL/TLS以支持HTTPS访问)</td><td>12345/80/443</td>
<tr><td>--product-env</td><td>是否为生产环境。生产环境下默认端口为80/443，并且会使用gevent和WSGIServer提高性能，如果要开启，用法为--product-env y</td> <td>默认关闭</td></tr>
<tr><td>--enable-ssl</td><td>是否开启HTTPS访问的支持。如果开启，用法为--enable-ssl y，并且需要指定--ssl-cert和--ssl-key两个参数。</td><td>默认关闭</td></tr>
<tr><td>--ssl-cert</td><td>cert.pem文件路径</td><td>空</td></tr>
<tr><td>--ssl-key</td><td>key.pem文件路径</td><td>空</td></tr>
<tr><td>--sql-server</td><td>SQL服务的地址:端口</td><td>localhost:3306</td></tr>
<tr><td>--sql-engine</td><td>SQL引擎</td><td>mysql+pymysql</td></tr>
<tr><td>--sql-user</td><td>SQL用户名</td><td>空，需要指定</td></tr>
<tr><td>--sql-passwd</td><td>SQL用户密码</td><td>空，需要指定</td></tr>
<tr><td>--sql-dbname</td><td>SQL数据库库名</td><td>TransportationGame</td></tr>
</tbody>
</table>