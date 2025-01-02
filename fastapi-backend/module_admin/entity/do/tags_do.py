from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from config.database import Base


class Tags(Base):
    """
    分类标签信息表
    """

    __tablename__ = 'tags'

    tags_id = Column(Integer, primary_key=True, autoincrement=True, comment='标签ID')
    tags_code = Column(String(64), nullable=False, comment='标签编码')
    tags_name = Column(String(50), nullable=False, comment='标签名称')
    tags_sort = Column(Integer, nullable=False, comment='显示顺序')
    avatar = Column(String(255), nullable=False, comment='标签图标地址')
    position = Column(String(30), nullable=False, comment='展示位置')
    status = Column(String(1), nullable=False, default='0', comment='状态（0正常 1停用）')
    create_by = Column(String(64), default='', comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now(), comment='创建时间')
    update_by = Column(String(64), default='', comment='更新者')
    update_time = Column(DateTime, nullable=True, default=datetime.now(), comment='更新时间')
    remark = Column(String(500), nullable=True, default=None, comment='备注')
