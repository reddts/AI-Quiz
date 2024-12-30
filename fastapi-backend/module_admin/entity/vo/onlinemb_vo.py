from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class OnlinembModel(BaseModel):
    """
    在线会员对应pydantic模型
    """

    token_id: Optional[str] = Field(default=None, description='会话编号')
    member_name: Optional[str] = Field(default=None, description='会员名称')
    visit_name: Optional[str] = Field(default=None, description='访问内容')
    ipaddr: Optional[str] = Field(default=None, description='登录IP地址')
    login_location: Optional[str] = Field(default=None, description='登录地址')
    browser: Optional[str] = Field(default=None, description='浏览器类型')
    os: Optional[str] = Field(default=None, description='操作系统')
    login_time: Optional[datetime] = Field(default=None, description='登录时间')


class OnlinembQueryModel(OnlinembModel):
    """
    在线会员不分页查询模型
    """

    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


class OnlinembPageQueryModel(OnlinembQueryModel):
    """
    在线会员分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteOnlinembModel(BaseModel):
    """
    强退在线会员模型
    """

    token_ids: str = Field(description='需要强退的会话编号')
