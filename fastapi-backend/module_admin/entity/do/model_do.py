from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from config.database import Base


class AiModel(Base):
    """
    模型信息表
    """

    __tablename__ = 'ai_model'

    model_id = Column(Integer, primary_key=True, autoincrement=True, comment='模型ID')
    model_name = Column(String(64), nullable=False, comment='模型编码')
    model_alias = Column(String(64), nullable=False, comment='模型名称')
    type_id = Column(Integer, nullable=False, comment='分类id')
    status = Column(String(1), nullable=False, default='0', comment='状态（0正常 1停用）')
    current = Column(String(1), nullable=False, default='0', comment='当前（0非当前 1当前）')
    context_num = Column(Integer, nullable=False, comment='上下文对话数')
    maxtoken = Column(Integer, nullable=False, comment='上下文最大token数')
    temperature = Column(Integer, nullable=False, comment='随机性')
    frequency = Column(Integer, nullable=False, comment='重复性')
    presence = Column(Integer, nullable=False, comment='创新性')
    create_by = Column(String(64), default='', comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now(), comment='创建时间')
    update_by = Column(String(64), default='', comment='更新者')
    update_time = Column(DateTime, nullable=True, default=datetime.now(), comment='更新时间')
    remark = Column(String(500), nullable=True, default=None, comment='备注')
