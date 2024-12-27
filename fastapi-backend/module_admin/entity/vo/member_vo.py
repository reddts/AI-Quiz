import re
from pydantic import BaseModel,ConfigDict, EmailStr, Field, model_validator
from pydantic_validation_decorator import Network, NotBlank, Size, Xss
from typing import Optional,Literal, Union
from datetime import datetime
from exceptions.exception import ModelValidatorException

class MemberModel(BaseModel):
    """
    会员表对应pydantic模型
    """
    model_config = ConfigDict(from_attributes=True)

    member_id: Optional[int] = Field(None, description="会员ID")
    member_name: Optional[str] = Field(None, max_length=100, description="会员姓名")
    nick_name: Optional[str] = Field(default=None, description='会员昵称')
    avatar: Optional[str] = Field(default=None, description='头像地址')
    password: Optional[str] = Field(default=None, description='密码')
    status: Optional[Literal['0', '1']] = Field(default=None, description='帐号状态（0正常 1停用）')
    age: Optional[int] = Field(None, description="会员年龄")
    gender: Optional[Literal['0', '1', '2']] = Field(default=None, description='会员性别（0男 1女 2未知）')
    email: Optional[EmailStr] = Field(None, description="会员邮箱")    
    phonenumber: Optional[str] = Field(default=None, description='手机号码')
    del_flag: Optional[int] = Field(default=0, description="会员ID")
    birthday:  Optional[datetime] = Field(default=None, description='生日')
    login_ip: Optional[str] = Field(default=None, description='最后登录IP')
    login_date: Optional[datetime] = Field(default=None, description='最后登录时间')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_at: Optional[datetime] = Field(None, description="创建时间")
    update_at: Optional[datetime] = Field(default=None, description='更新时间')
    update_by: Optional[str] = Field(default=None, description='更新者')    
    remark: Optional[str] = Field(default=None, description='备注')

    @model_validator(mode='after')
    def check_password(self) -> 'MemberModel':
        pattern = r"""^[^<>"'|\\]+$"""
        if self.password is None or re.match(pattern, self.password):
            return self
        else:
            raise ModelValidatorException(message='密码不能包含非法字符：< > " \' \\ |')


    @Xss(field_name='member_name', message='会员账号不能包含脚本字符')
    @NotBlank(field_name='member_name', message='会员账号不能为空')
    @Size(field_name='member_name', min_length=3, max_length=30, message='会员账号长度必须在3到30个字符之间')
    def get_member_name(self):
        return self.member_name

    @Xss(field_name='nick_name', message='会员昵称不能包含脚本字符')
    @Size(field_name='nick_name', min_length=0, max_length=30, message='会员昵称长度不能超过30个字符')
    def get_nick_name(self):
        return self.nick_name

    @Network(field_name='email', field_type='EmailStr', message='邮箱格式不正确')
    @Size(field_name='email', min_length=0, max_length=50, message='邮箱长度不能超过50个字符')
    def get_email(self):
        return self.email

    @Size(field_name='phonenumber', min_length=0, max_length=11, message='手机号码长度不能超过11个字符')
    def get_phonenumber(self):
        return self.phonenumber

    def validate_fields(self):
        self.get_member_name()
        self.get_nick_name()
        self.get_email()
        self.get_phonenumber()

class MemberInfoModel(MemberModel):
    """
    获取会员详情信息响应模型
    """
    

class CreateMemberModel(MemberModel):
    """
    创建会员对应pydantic模型
    """
    type: Optional[str] = Field(default=None, description='操作类型')

class EditMemberModel(CreateMemberModel):
    """
    编辑会员模型
    """

class DeleteMemberModel(BaseModel):
    """
    删除会员模型
    """
    member_ids: str = Field(description='需要删除的会员ID')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_at: Optional[datetime] = Field(default=None, description='更新时间')


class MemberQueryModel(MemberModel):
    """
    会员管理不分页查询模型
    """

    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


class MemberPageQueryModel(MemberQueryModel):
    """
    会员管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')

class MemberProfileModel(BaseModel):
    """
    获取会员信息响应模型
    """

    data: Union[MemberInfoModel, None] = Field(description='会员信息')