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

    member_id: Optional[int] = Field(None, description="用户ID")
    member_name: Optional[str] = Field(None, max_length=100, description="用户姓名")
    nick_name: Optional[str] = Field(default=None, description='用户昵称')
    avatar: Optional[str] = Field(default=None, description='头像地址')
    password: Optional[str] = Field(default=None, description='密码')
    status: Optional[Literal['0', '1']] = Field(default=None, description='帐号状态（0正常 1停用）')
    age: Optional[int] = Field(None, description="用户年龄")
    gender: Optional[str] = Field(None, description="用户性别", regex="^(M|F)$")
    email: Optional[EmailStr] = Field(None, description="用户邮箱")
    phonenumber: Optional[str] = Field(default=None, description='手机号码')
    login_ip: Optional[str] = Field(default=None, description='最后登录IP')
    login_date: Optional[datetime] = Field(default=None, description='最后登录时间')
    created_at: Optional[datetime] = Field(None, description="创建时间")
    update_at: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')

    @model_validator(mode='after')
    def check_password(self) -> 'MemberModel':
        pattern = r"""^[^<>"'|\\]+$"""
        if self.password is None or re.match(pattern, self.password):
            return self
        else:
            raise ModelValidatorException(message='密码不能包含非法字符：< > " \' \\ |')


    @Xss(field_name='member_name', message='用户账号不能包含脚本字符')
    @NotBlank(field_name='member_name', message='用户账号不能为空')
    @Size(field_name='member_name', min_length=0, max_length=30, message='用户账号长度不能超过30个字符')
    def get_member_name(self):
        return self.member_name

    @Xss(field_name='nick_name', message='用户昵称不能包含脚本字符')
    @Size(field_name='nick_name', min_length=0, max_length=30, message='用户昵称长度不能超过30个字符')
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

class UserDetailModel(BaseModel):
    """
    获取用户详情信息响应模型
    """

    data: Optional[Union[str, None]] = Field(default=None, description='用户信息')
    

class CreateMemberVO(BaseModel):
    """
    创建会员对应pydantic模型
    """
    name: Optional[str] = Field(None, max_length=100, description="用户姓名")
    age: Optional[int] = Field(None, description="用户年龄")
    gender: Optional[str] = Field(None, description="用户性别", regex="^(M|F)$")
    email: Optional[EmailStr] = Field(None, description="用户邮箱")

    class Config:
        orm_mode = True

class UpdateMemberVO(BaseModel):
    """
    更新会员对应pydantic模型
    """    
    name: Optional[str] = Field(None, max_length=100, description="用户姓名")
    age: Optional[int] = Field(None, description="用户年龄")
    gender: Optional[str] = Field(None, description="用户性别", regex="^(M|F)$")
    email: Optional[EmailStr] = Field(None, description="用户邮箱")

    class Config:
        orm_mode = True

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