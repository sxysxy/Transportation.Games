from sqlalchemy import create_engine, Column, String, PrimaryKeyConstraint, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建引擎，连接到MySQL数据库，替换以下信息为你的MySQL连接信息
engine = create_engine('mysql+pymysql://username:password@localhost:3306/TransportationGames')

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
    phone_number = Column(String(20), nullable=False)
    organization = Column(String(100), nullable=False)
    model_name = Column(String(100), nullable=False)

    # 添加主键约束
    PrimaryKeyConstraint('email', name='email_pk')

# 创建表，将用户模型映射到数据库中
Base.metadata.create_all(engine)

# 创建会话，用于与数据库进行交互
Session = sessionmaker(bind=engine)
session = Session()

# 用户注册函数
def register(email, username, password, confirm_password, phone_number, organization, model_name):

  # 判断两次输入密码是否相同
  if password != confirm_password:
    print("Two inputs of passwords are different!")
    return 

  # 创建新用户对象
  new_user = User(email=email, 
                  username=username,
                  password=password,
                  confirm_password=confirm_password,
                  phone_number=phone_number,
                  organization=organization,
                  model_name=model_name)
                  
  # 添加到数据库会话
  session.add(new_user)

  # 提交事务到数据库
  session.commit()

  print(f"User {email} has been registered successfully!")

# 示例:注册新用户  
email = 'newuser@example.com'
username = 'newuser'
password = '123456'
confirm_password = '123456'
phone_number = '12345678901'
organization = 'Anthropic'
model_name = 'Claude'

register(email, username, password, confirm_password, phone_number, organization, model_name)

def login(email, password):
    # 查询用户
    user = session.query(User).filter_by(email=email, password=password).first()

    # 验证用户是否存在且密码匹配
    if user:
        print(f"Login successful for user {user.email}")
        return True
    else:
        print("Login failed. Incorrect email or password.")
        return False

# 示例：尝试登录
user_email = 'user@example.com'
user_password = 'password123'

login(user_email, user_password)