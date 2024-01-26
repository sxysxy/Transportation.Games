from sqlalchemy import create_engine, Table, MetaData, Column, String, Index, Integer, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#声明基类，所有的实体类都应该继承自Base
Base = declarative_base()

# 定义用户模型，表示数据库中的用户表结构
class User(Base):
    # 表名
    __tablename__ = 'users'
    
    # 列定义，包括主键（邮箱）、用户名、密码、确认密码、手机号、发布机构、模型名称
    
    userid = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=False)
    username = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    organization = Column(String(100), nullable=False)
    # model_name = Column(String(100), nullable=False)

    # 添加主键约束
    __table_args__ = (
        PrimaryKeyConstraint('userid', name='userid_pk'),
       # Index('index_by_email', 'email')
    )  
    
    
class DataModel:
    def __init__(self, sql_engine_name, sql_server, sql_username, sql_password, sql_dbname) -> None:
        if ':' in sql_server:
            host, port = sql_server.split(':')
        else:
            host = sql_server
            port = 3306
            
        self.engine = create_engine(f"{sql_engine_name}://", 
                                    connect_args={
                                        'host' : host,
                                        'port' : int(port),
                                        'user' : sql_username,
                                        'password' : sql_password,
                                        'database' : sql_dbname,
                                        #'charset' : 'utf-8'
                                    })
        
         
        # 创建表，将用户模型映射到数据库中
        Base.metadata.create_all(self.engine)
        
        # 创建会话，用于与数据库进行交互
        Session = sessionmaker(bind=self.engine)
        self._session = Session()
        
    @property
    def session(self):
        return self._session
    
    # 用户注册函数
    def user_register(self, **user_info):
        # 创建新用户对象
        new_user = User(**user_info)
                    
        # 添加到数据库会话
        self.session.add(new_user)

        # 提交事务到数据库
        self.session.commit()
            
    def user_auth(self, userid, password):
        # 查询用户
        user = self.session.query(User).filter_by(userid=userid).first()

        # 验证用户是否存在且密码匹配
        if user and user.password == password:
            return True
        else:
            return False
        
    def user_check_id_available(self, userid):
        return self.session.query(User).filter_by(userid=userid).first() is None