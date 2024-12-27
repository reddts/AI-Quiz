from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime


class Member(Base):
    """
    会员信息表
    """
    __tablename__ = 'member'

    member_id = Column(Integer, primary_key=True, autoincrement=True, comment='会员ID')
    member_name = Column(String(100), default=None, comment='会员姓名')
    nick_name = Column(String(30), nullable=False, comment='会员昵称')
    avatar = Column(String(100), default='', comment='头像地址')
    password = Column(String(100), default='', comment='密码')
    age = Column(Integer, default=None, comment='会员年龄')
    gender = Column(String(1), default='0', comment='会员性别（0男 1女 2未知）')
    email = Column(String(100), default=None, comment='会员邮箱')
    birthday = Column(String(100), comment='生日', default=None)
    phonenumber = Column(String(11), default='', comment='手机号码')
    status = Column(String(1), default='0', comment='帐号状态（0正常 1停用）')
    del_flag = Column(String(1), default='0', comment='删除标志（0代表存在 2代表删除）')
    login_ip = Column(String(128), default='', comment='最后登录IP')
    login_date = Column(DateTime, comment='最后登录时间')
    remark = Column(String(500), default=None, comment='备注')
    create_at = Column(DateTime, comment='创建时间', default=datetime.now())
    create_by = Column(String(100), default=None, comment='创建者')
    update_at = Column(DateTime, comment='更新时间', default=datetime.now())
    update_by = Column(String(100), default=None, comment='修改者')
    
    # Relationships
    #recommendations = relationship("MemberAIRecommendations", back_populates="member")
    #scale_answers = relationship("MemberScaleAnswers", back_populates="member")