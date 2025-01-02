from datetime import datetime
from sqlalchemy import Column, Text, DateTime, Integer, String
from config.database import Base


class Scales(Base):
    """
    量表信息表
    """

    __tablename__ = 'scales'

    scales_id = Column(Integer, primary_key=True, autoincrement=True, comment='量表ID')
    title = Column(String(64), nullable=False, comment='量表名称')
    snippet = Column(String(255), nullable=False, comment='量表简介')
    descrition = Column(Text, nullable=False, comment='量表简介')
    scales_sort = Column(Integer, nullable=False, comment='显示顺序')
    avatar = Column(String(255), nullable=False, comment='图标地址')
    visit = Column(Integer, nullable=False, comment='访问量')
    status = Column(String(1), nullable=False, default='0', comment='状态（0正常 1停用）')
    create_by = Column(String(64), default='', comment='创建者')
    create_at = Column(DateTime, nullable=True, default=datetime.now(), comment='创建时间')
    update_by = Column(String(64), default='', comment='更新者')
    update_at = Column(DateTime, nullable=True, default=datetime.now(), comment='更新时间')
    del_flag = Column(String(1), default='0', comment='删除标志（0代表存在 2代表删除）')


class ScalesTags(Base):
    """
    量表与标签关联表
    """

    __tablename__ = 'scales_tags'

    scales_id = Column(Integer, primary_key=True, nullable=False, comment='量表ID')
    tags_id = Column(Integer, primary_key=True, nullable=False, comment='标签ID')