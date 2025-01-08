from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from config.database import Base


class Keypool(Base):
    """
    key池信息表
    """

    __tablename__ = 'ai_keypool'

    key_id = Column(Integer, primary_key=True, autoincrement=True, comment='标签ID')
    key_name = Column(String(50), nullable=False, comment='key的名称')
    key_typeid = Column(Integer, nullable=False, comment='key的分类')
    key_token = Column(String(255), nullable=False, comment='keytoken')
    disablereason = Column(String(255), nullable=False, comment='停用原因')
    status = Column(String(1), nullable=False, default='0', comment='状态（0正常 1停用）')
    create_by = Column(String(64), default='', comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now(), comment='创建时间')
    update_by = Column(String(64), default='', comment='更新者')
    update_time = Column(DateTime, nullable=True, default=datetime.now(), comment='更新时间')
    remark = Column(String(500), nullable=True, default=None, comment='备注')
