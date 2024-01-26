# Transportation.Games
论文 <a href="https://arxiv.org/abs/2401.04471">TransportationGames: Benchmarking Transportation Knowledge of Multimodal Large Language Models</a> 的宣传网站的源代码

# 下载&安装

```
git clone git@github.com:sxysxy/Transportation.Games.git 
```

或者使用HTTPS方式clone 

```
git clone https://github.com/sxysxy/Transportation.Games.git
```

然后准备一个虚拟环境，python版本可以使用3.11（仅供参考）

```
conda activate your_virtual_env
pip install -r requirements.txt
```

# 运行

### SQL数据库准备

在mysql数据库运行sql语句建库
```
CREATE DATABASE TransportationGames
    DEFAULT CHARACTER SET = 'utf8mb4';
```
将main.py中创建引擎的相关信息替换为Mysql连接信息
```
engine = create_engine('mysql+pymysql://user:password@localhost:3306/TransportationGames')
```

### 服务端程序运行

服务端程序有两个，main.py为主站的程序，backend.py为后台管理界面的程序。主站和后台管理界面程序是分开的，但是可以共用一个数据库。以main.py为例:

在开发与调试环境下：

```
python main.py
```

默认网络端口是12345

如果是生产环境中：

```
python main.py --product-env y
```

指定该参数则会使用gevent.monkey.patch_all()和WSGIServer来提高Flask App的性能。默认的端口也会变成80或者443（取决于你是否开启了HTTPS支持）

注意，实际上还需要指定数据库的参数，否则登录、后台管理等功能无法正常使用，仅能够浏览主页index.html

# 内容定制

为主页添加文本内容：在主页Markdown.md里直接编辑  
为排行榜添加文本内容：在排行榜Markdown.md里直接编辑

# 程序命令行参数

以下命令行参数，main.py与backend.py通用。main.py启动主站服务，backend.py启动后台管理网站服务。

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
<tr><td>--sql-engine</td><td>SQL引擎，例如'mysql+pymysql'、'mariadb+mariadbconnector'等</td><td>mysql+pymysql</td></tr>
<tr><td>--sql-user</td><td>SQL用户名</td><td>空，需要指定</td></tr>
<tr><td>--sql-passwd</td><td>SQL用户密码</td><td>空，需要指定</td></tr>
<tr><td>--sql-dbname</td><td>SQL数据库库名</td><td>TransportationGame</td></tr>
</tbody>
</table>

# 开源软件协议

本网站项目使用的开源软件协议是LGPL-3。您可以自由地、免费地使用该项目，但如果基于本项目的开源程序代码公开发布新的项目，则必须同样以LGPL-3协议开源。

此外，以下是源代码内嵌在本项目内的其他开源程序代码：

<table>
<tbody>
<tr> <td>jquery</td> </td> <td> MIT协议 </td> </tr>
<tr> <td>Semantic-UI</td> <td> MIT协议 </tr>
</tobyd>
</table>
