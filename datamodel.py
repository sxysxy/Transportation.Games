from sqlalchemy import create_engine, Column, String, PrimaryKeyConstraint, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 声明基类，所有的实体类都应该继承自Base
Base = declarative_base()

# 定义用户模型，表示数据库中的用户表结构
class User(Base):
    # 表名
    __tablename__ = 'users'
    
    # 列定义，包括主键（邮箱）、用户名、密码、确认密码、手机号、发布机构、模型名称
    email = Column(String(100), primary_key=True, nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    confirm_password = Column(String(50), nullable=False)  # 确认密码字段
    # phone_number = Column(String(20), nullable=False)
    # organization = Column(String(100), nullable=False)
    # model_name = Column(String(100), nullable=False)

    # 添加主键约束
    PrimaryKeyConstraint('email', name='email_pk')
    
class DataModel:
    def __init__(self, sql_path) -> None:
        self.engine = create_engine(sql_path)
        # 创建会话，用于与数据库进行交互
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        # 创建表，将用户模型映射到数据库中
        Base.metadata.create_all(self.engine)
    
    # 用户注册函数
    def registeruser(self, username, password, confirm_password, email, ):

        # 判断两次输入密码是否相同
        if password != confirm_password:
            print("Two inputs of passwords are different!")
            return 

        # 创建新用户对象
        new_user = User( 
                        username=username,
                        password=password,
                        confirm_password=confirm_password,
                        email=email,
                        # phone_number=phone_number,
                        # organization=organization,
                        # model_name=model_name
                        )
                    
        # 添加到数据库会话
        self.session.add(new_user)

        # 提交事务到数据库
        self.session.commit()

        print(f"User {email} has been registered successfully!")


    def loginuser(self,username, password):
        # 查询用户
        user = self.session.query(User).filter_by(username=username, password=password).first()

        # 验证用户是否存在且密码匹配
        if user:
            print(f"Login successful for user {user.username}")
            return True
        else:
            print("Login failed. Incorrect username or password.")
            return False