from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic_validation_decorator import NotBlank, Size
from typing import Literal, Optional


class ModeltypeModel(BaseModel):
    """
    模型分类信息表对应pydantic模型
    """

    model_config = ConfigDict(from_attributes=True)

    type_id: Optional[int] = Field(default=None, description='模型分类ID')
    type_name: Optional[str] = Field(default=None, description='模型分类名称')
    api_url: Optional[str] = Field(default=None, description='模型api地址')
    status: Optional[Literal['0', '1']] = Field(default=None, description='状态（0正常 1停用）')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')

    @NotBlank(field_name='type_name', message='模型分类名称不能为空')
    @Size(field_name='type_name', min_length=0, max_length=64, message='模型分类名称长度不能超过64个字符')
    def get_type_name(self):
        return self.type_name

    @NotBlank(field_name='api_url', message='模型分类api url不能为空')
    @Size(field_name='api_url', min_length=0, max_length=200, message='模型分类api url长度不能超过200个字符')
    def get_apiurl(self):
        return self.api_url


    def validate_fields(self):
        self.get_type_name()
        self.get_apiurl()


class ModeltypeQueryModel(ModeltypeModel):
    """
    模型分类管理不分页查询模型
    """

    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


class ModeltypePageQueryModel(ModeltypeQueryModel):
    """
    模型分类管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteModeltypeModel(BaseModel):
    """
    删除模型分类模型
    """

    type_ids: str = Field(description='需要删除的模型分类ID')
