from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic_validation_decorator import NotBlank, Size
from typing import Literal, Optional


class TagsModel(BaseModel):
    """
    分类标签信息表对应pydantic模型
    """

    model_config = ConfigDict(from_attributes=True)

    tags_id: Optional[int] = Field(default=None, description='标签ID')
    tags_code: Optional[str] = Field(default=None, description='标签编码')
    tags_name: Optional[str] = Field(default=None, description='标签名称')
    tags_sort: Optional[int] = Field(default=None, description='显示顺序')
    avatar: Optional[str] = Field(default=None, description='标签图标地址')
    position: Optional[str] = Field(default=None, description='展示位置')
    status: Optional[Literal['0', '1']] = Field(default=None, description='状态（0正常 1停用）')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')

    @NotBlank(field_name='tags_code', message='标签编码不能为空')
    @Size(field_name='tags_code', min_length=0, max_length=64, message='标签编码长度不能超过64个字符')
    def get_tags_code(self):
        return self.tags_code

    @NotBlank(field_name='tags_name', message='标签名称不能为空')
    @Size(field_name='tags_name', min_length=0, max_length=50, message='标签名称长度不能超过50个字符')
    def get_tags_name(self):
        return self.tags_name

    @NotBlank(field_name='tags_sort', message='显示顺序不能为空')
    def get_tags_sort(self):
        return self.tags_sort

    def validate_fields(self):
        self.get_tags_code()
        self.get_tags_name()
        self.get_tags_sort()


class TagsQueryModel(TagsModel):
    """
    分类标签管理不分页查询模型
    """

    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


class TagsPageQueryModel(TagsQueryModel):
    """
    分类标签管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteTagsModel(BaseModel):
    """
    删除分类标签模型
    """

    tags_ids: str = Field(description='需要删除的标签ID')
