from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic_validation_decorator import NotBlank, Size
from typing import Literal, Optional


class KeypoolModel(BaseModel):
    """
    key池信息表对应pydantic模型
    """

    model_config = ConfigDict(from_attributes=True)

    key_id: Optional[int] = Field(default=None, description='key池ID')
    key_name: Optional[str] = Field(default=None, description='key池名称')
    key_typeid: Optional[int] = Field(default=None, description='分类id')
    key_token: Optional[str] = Field(default=None, description='keytoken')
    disablereason: Optional[str] = Field(default=None, description='停用原因')
    status: Optional[Literal['0', '1']] = Field(default=None, description='状态（0正常 1停用）')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')

    @NotBlank(field_name='key_name', message='key池名称不能为空')
    @Size(field_name='key_name', min_length=0, max_length=50, message='key池名称长度不能超过50个字符')
    def get_keypool_name(self):
        return self.key_name

    def validate_fields(self):
        self.get_keypool_name()


class KeypoolQueryModel(KeypoolModel):
    """
    key池管理不分页查询模型
    """

    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


class KeypoolPageQueryModel(KeypoolQueryModel):
    """
    key池管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteKeypoolModel(BaseModel):
    """
    删除key池模型
    """

    key_ids: str = Field(description='需要删除的key池ID')
