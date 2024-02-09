# Transportation.Games
论文 <a href="https://arxiv.org/abs/2401.04471">TransportationGames: Benchmarking Transportation Knowledge of Multimodal Large Language Models</a> 的宣传网站的源代码。易于定制自己的内容，可以当做一个模板套用到其他类似的项目上。

<div style="font-size:32px">目录</div>

- [Transportation.Games](#transportationgames)
- [下载\&安装](#下载安装)
- [运行](#运行)
    - [SQL数据库准备](#sql数据库准备)
    - [服务端程序运行](#服务端程序运行)
- [内容定制](#内容定制)
- [程序命令行参数](#程序命令行参数)
- [使用其他数据库](#使用其他数据库)
- [HTTPS访问支持](#https访问支持)
- [Nginx](#nginx)
- [其他](#其他)
- [开源软件协议](#开源软件协议)


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

数据库名字也可以用别的，可以对main.py的命令行参数--sql-dbname做修改实现，可以但没必要= =。

### 服务端程序运行

服务端程序有两个，main.py为主站的程序，backend.py为后台管理界面的程序。主站和后台管理界面程序是分开的，但是可以共用一个数据库。以main.py为例:

在开发与调试环境下：

```
python main.py --sql-user 你的sql用户名 --sql-passwd 你的sql的密码
```

默认网络端口是12345

如果是生产环境中则可以加入下面这个参数：

```
--product-env y
```

指定该参数则会使用gevent.monkey.patch_all()和WSGIServer来提高Flask App的性能。默认的端口也会变成80或者443（取决于你是否开启了HTTPS支持）

以及如果公开发布网站

```
--icp-license 某ICP备XXXXXXXXXX号
```

可以在网页底部显示ICP号。


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
<tr><td>--sql-dbname</td><td>SQL数据库库名</td><td>TransportationGames</td></tr>
<tr><td>--icp-license</td><td>字符串，按照 某ICP备XXXXXXXX号 的格式（位数不一定）</td><td>空，如果不指定，则不显示icp备案信息</td></tr>
<tr><td>--forward-http2https</td><td>是否开启HTTP到HTTPS的自动重定向服务。这个选项只在服务器为Linux/MacOS时有效，windows上不起作用。开启添加参数--forward-http2https y即可。这个参数也需要--enable-ssl y才有效。</td><td>默认关闭</td><td></td></tr>
<tr><td>--forward-http-port</td><td>在开启SSL支持的时候如果同时开启了HTTP访问对HTTPS的重定向，则这里指定HTTP服务使用的端口号。</td><td>80</td></tr>
</tbody>
</table>

# 使用其他数据库

实测mysql、Linux上的mariadb无需修改运行命令行参数

在macos上使用mariadb则需要pip安装mariadb包并且添加命令行参数

```
--sql-engine "mariadb+mariadbconnector"
```

其他的SQL数据库实现请查询SQLAlchemy的文档。


# HTTPS访问支持

需要获得证书和密钥文件，加入参数

```
--enable-ssl y --ssl-cert 证书文件 --ssl-key 密钥文件
```

就可以开启HTTPS访问，同时不支持HTTP访问。

如果需要开启HTTP到HTTPS的重定向，可以添加参数

```
--forward-http2https y --forward-http-port 80
```

80是默认http服务所用端口，如果你是用的不是80就替换掉

# Nginx

当然也可以配合nginx使用，并且项目中有一个generate_nginx_conf.py帮助生成nginx配置，因为代码很简单可以直接打开看看不详细介绍。

# 其他

项目的.gitignore中有SSLCerts文件夹，nginx.conf，start_website.sh，所以可以自己编写start_website.sh来添加命令行参数启动网页服务，SSLCerts文件夹内存放SSL证书等。

# 开源软件协议

本网站项目使用的开源软件协议是LGPL-3。您可以自由地、免费地使用该项目，但如果基于本项目的开源程序代码公开发布新的项目，则必须同样以LGPL-3协议开源。

此外，以下是源代码内嵌在本项目内的其他开源程序代码：

<table>
<tbody>
<tr> <td>jquery</td> </td> <td> MIT协议 </td> </tr>
<tr> <td>Semantic-UI</td> <td> MIT协议 </tr>
</tobyd>
</table>
