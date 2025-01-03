from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic_validation_decorator import NotBlank, Size
from typing import Literal, Optional


class AiModelModel(BaseModel):
    """
    AI模型信息表对应pydantic模型
    """

    model_config = ConfigDict(from_attributes=True)

    model_id: Optional[int] = Field(default=None, description='模型ID')
    model_name: Optional[str] = Field(default=None, description='调用名称')
    model_alias: Optional[str] = Field(default=None, description='显示名称')
    type_id: Optional[int] = Field(default=None, description='分类id')
    current: Optional[Literal['0', '1']] = Field(default=None, description='当前标记（0非在用 1当前）')
    status: Optional[Literal['0', '1']] = Field(default=None, description='状态（0正常 1停用）')
    context_num: Optional[int] = Field(default=None, description='上下文对话数')
    maxtoken: Optional[int] = Field(default=None, description='上下文最大token数')
    temperature: Optional[int] = Field(default=None, description='随机性')
    frequency: Optional[int] = Field(default=None, description='重复性')
    presence: Optional[int] = Field(default=None, description='创新性')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')

    @NotBlank(field_name='model_name', message='模型调用名称不能为空')
    @Size(field_name='model_name', min_length=0, max_length=64, message='模型调用名称长度不能超过64个字符')
    def get_model_name(self):
        return self.model_name

    @NotBlank(field_name='model_alias', message='模型显示名称不能为空')
    @Size(field_name='model_alias', min_length=0, max_length=64, message='模型显示名称长度不能超过64个字符')
    def get_model_alias(self):
        return self.model_alias

    @NotBlank(field_name='type_id', message='模型分类不能为空')
    def get_type_id(self):
        return self.type_id

    def validate_fields(self):
        self.get_model_name()
        self.get_model_alias()
        self.get_type_id()


class AiModelQueryModel(AiModelModel):
    """
    分类模型管理不分页查询模型
    """

    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


class AiModelPageQueryModel(AiModelQueryModel):
    """
    分类模型管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteAiModelModel(BaseModel):
    """
    删除分类模型模型
    """

    model_ids: str = Field(description='需要删除的模型ID')
