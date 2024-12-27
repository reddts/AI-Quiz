import logging
import io
import pandas as pd
from datetime import datetime
from fastapi import Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Union
from exceptions.exception import ServiceException
from module_admin.dao.member_dao import MemberDao
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.member_vo import (
    CreateMemberModel,
    EditMemberModel,
    MemberModel,
    MemberPageQueryModel,
    MemberInfoModel,
    DeleteMemberModel,
    )
from module_admin.service.config_service import ConfigService
from module_admin.entity.vo.user_vo import CurrentUserModel
from config.constant import CommonConstant
from module_admin.entity.vo.common_vo import CrudResponseModel
from utils.page_util import PageResponseModel
from utils.common_util import export_list2excel, get_excel_template, SqlalchemyUtil
from utils.pwd_util import PwdUtil

logger = logging.getLogger(__name__)  # 日志记录器

class MemberService:
    """
    Member 服务层，提供业务逻辑处理功能
    """

#获取所有会员
    @classmethod
    async def get_member_list_services(
        cls, query_db: AsyncSession, query_object: MemberPageQueryModel,  is_page: bool = False
    ):
        """
        获取所有会员信息（支持分页）

        :param db: 数据库会话
        :param page: 当前页码
        :param size: 每页大小
        :return: 分页或全部会员信息的列表
        """
        query_result = await MemberDao.get_member_list(query_db, query_object,  is_page)
        if is_page:
            query_result_dict = query_result.model_dump()
            query_result_dict['rows'] = [row for row in query_result.rows]  # 移除 'dept' 字段
            member_list_result = PageResponseModel(**query_result_dict)
        else:
            member_list_result = []
            if query_result:
                member_list_result = [row for row in query_result]  # 移除 'dept' 字段

        return member_list_result

#检查会员账号名的唯一性
    @classmethod
    async def check_member_name_unique_services(cls, query_db: AsyncSession, page_object: MemberModel):
        """
        校验会员用户名是否唯一service

        :param query_db: orm对象
        :param page_object: 会员对象
        :return: 校验结果
        """
        member_id = -1 if page_object.member_id is None else page_object.member_id
        member = await MemberDao.get_member_by_info(query_db, MemberModel(member_name=page_object.member_name))
        if member and member.member_id != member_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

#检查电话号码的唯一性
    @classmethod
    async def check_phonenumber_unique_services(cls, query_db: AsyncSession, page_object: MemberModel):
        """
        校验会员手机号是否唯一service

        :param query_db: orm对象
        :param page_object: 会员对象
        :return: 校验结果
        """
        member_id = -1 if page_object.member_id is None else page_object.member_id
        member = await MemberDao.get_member_by_info(query_db, MemberModel(phonenumber=page_object.phonenumber))
        if member and member.member_id != member_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

#检查email的唯一性
    @classmethod
    async def check_email_unique_services(cls, query_db: AsyncSession, page_object: MemberModel):
        """
        校验会员邮箱是否唯一service

        :param query_db: orm对象
        :param page_object: 会员对象
        :return: 校验结果
        """
        member_id = -1 if page_object.member_id is None else page_object.member_id
        member = await MemberDao.get_member_by_info(query_db, MemberModel(email=page_object.email))
        if member and member.member_id != member_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

#新增会员服务
    @classmethod
    async def add_member_services(cls, query_db: AsyncSession, page_object: CreateMemberModel):
        """
        新增会员信息service

        :param query_db: orm对象
        :param page_object: 新增会员对象
        :return: 新增会员校验结果
        """
        add_member = MemberModel(**page_object.model_dump())
        if not await cls.check_member_name_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增会员{page_object.member_name}失败，账号已存在')
        elif page_object.phonenumber and not await cls.check_phonenumber_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增会员{page_object.member_name}失败，手机号码已存在')
        elif page_object.email and not await cls.check_email_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增会员{page_object.member_name}失败，邮箱账号已存在')
        else:
            try:
                await MemberDao.add_member_dao(query_db, add_member)                
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='新增成功')
            except Exception as e:
                await query_db.rollback()
                raise e

#编辑会员服务
    @classmethod
    async def edit_member_services(cls, query_db: AsyncSession, page_object: EditMemberModel):
        """
        编辑会员信息service

        :param query_db: orm对象
        :param page_object: 编辑会员对象
        :return: 编辑会员校验结果
        """
        edit_member = page_object.model_dump(exclude_unset=True)
        if page_object.type == 'status' or page_object.type == 'avatar' or page_object.type == 'pwd':
            del edit_member['type']
        member_info = await cls.member_detail_services(query_db, edit_member.get('member_id'))
        if member_info and member_info.member_id:
            if page_object.type != 'status' and page_object.type != 'avatar' and page_object.type != 'pwd':
                if not await cls.check_member_name_unique_services(query_db, page_object):
                    raise ServiceException(message=f'修改会员{page_object.user_name}失败，账号已存在')
                elif page_object.phonenumber and not await cls.check_phonenumber_unique_services(query_db, page_object):
                    raise ServiceException(message=f'修改会员{page_object.user_name}失败，手机号码已存在')
                elif page_object.email and not await cls.check_email_unique_services(query_db, page_object):
                    raise ServiceException(message=f'修改会员{page_object.user_name}失败，邮箱账号已存在')
            try:
                await MemberDao.edit_member_dao(query_db, edit_member)                
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='会员不存在')

#获取会员详细信息服务
    @classmethod
    async def member_detail_services(cls, query_db: AsyncSession, member_id: Union[int, str]):
        """
        获取用户详细信息service

        :param query_db: orm对象
        :param member_id: 会员id
        :return: 会员id对应的信息
        """
        if member_id != '':
            query_member = await MemberDao.get_member_detail_by_id(query_db, member_id=member_id)
            if query_member:
                result = MemberModel(**SqlalchemyUtil.serialize_result(query_member))
            else:
                result = MemberModel(**dict())

        return result

#删除会员服务
    @classmethod
    async def delete_member_services(cls, query_db: AsyncSession, page_object: DeleteMemberModel):
        """
        删除会员信息service

        :param query_db: orm对象
        :param page_object: 删除会员对象
        :return: 删除会员校验结果
        """
        if page_object.member_ids:
            member_id_list = page_object.member_ids.split(',')
            try:
                for member_id in member_id_list:
                    member_id_dict = dict(
                        member_id=member_id, update_by=page_object.update_by, update_at=page_object.update_at
                    )                    
                    await MemberDao.delete_member_dao(query_db, MemberModel(**member_id_dict))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入会员id为空')

#批量导入会员服务
    @classmethod
    async def batch_import_member_services(
        cls,
        request: Request,
        query_db: AsyncSession,
        file: UploadFile,
        update_support: bool,
        current_user: CurrentUserModel,
    ):
        """
        批量导入会员service

        :param request: Request对象
        :param query_db: orm对象
        :param file: 会员导入文件对象
        :param update_support: 用户存在时是否更新
        :param current_user: 当前用户对象
        :return: 批量导入会员结果
        """
        header_dict = {            
            '登录名称': 'member_name',
            '会员名称': 'nick_name',
            '会员邮箱': 'email',
            '手机号码': 'phonenumber',
            '会员性别': 'gender',
            '会员生日': 'birthday',
            '帐号状态': 'status',
            '备    注': 'remark',
        }
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        await file.close()
        df.rename(columns=header_dict, inplace=True)
        add_error_result = []
        count = 0
        try:
            for index, row in df.iterrows():
                count = count + 1
                row['gender'] = {'男': '0', '女': '1', '未知': '2'}.get(row['gender'], row['gender'])
                row['status'] = {'正常': '0', '停用': '1'}.get(row['status'], row['status'])
                add_member = MemberModel(                    
                    member_name=row['member_name'],
                    password=PwdUtil.get_password_hash(
                        await ConfigService.query_config_list_from_cache_services(
                            request.app.state.redis, 'sys.user.initPassword'
                        )
                    ),
                    nick_name=row['nick_name'],
                    email=row['email'],
                    phonenumber=str(row['phonenumber']),
                    gender=row['gender'],
                    birthday=row['birthday'],
                    status=row['status'],
                    create_by=current_user.user.user_name,
                    create_at=datetime.now(),
                    update_by=current_user.user.user_name,
                    update_at=datetime.now(),
                    remark=row['remark'],
                )
                member_info = await MemberDao.get_member_by_info(query_db, MemberModel(user_name=row['member_name']))
                if member_info:
                    if update_support:
                        edit_member_model = MemberModel(
                            member_id=member_info.member_id,
                            member_name=row['member_name'],
                            nick_name=row['nick_name'],
                            email=row['email'],
                            phonenumber=str(row['phonenumber']),
                            gender=row['gender'],
                            birthday=row['birthday'],
                            remark=row['remark'],
                            status=row['status'],
                            update_by=current_user.user.user_name,
                            update_at=datetime.now(),
                        )
                        edit_member_model.validate_fields()                        
                        edit_member = edit_member_model.model_dump(exclude_unset=True)
                        await MemberDao.edit_member_dao(query_db, edit_member)
                    else:
                        add_error_result.append(f"{count}.会员账号{row['member_name']}已存在")
                else:
                    add_member.validate_fields()                    
                    await MemberDao.add_member_dao(query_db, add_member)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='\n'.join(add_error_result))
        except Exception as e:
            await query_db.rollback()
            raise e

#批量导入会员的模板        
    @staticmethod
    async def get_member_import_template_services():
        """
        获取会员导入模板service

        :return: 会员导入模板excel的二进制数据
        """
        header_list = ['登录名称', '会员名称', '会员邮箱', '手机号码', '会员性别', '会员生日','备注','帐号状态']
        selector_header_list = ['会员性别', '帐号状态']
        option_list = [{'会员性别': ['男', '女', '未知']}, {'帐号状态': ['正常', '停用']}]
        binary_data = get_excel_template(
            header_list=header_list, selector_header_list=selector_header_list, option_list=option_list
        )

        return binary_data

#批量导出会员模板    
    @staticmethod
    async def export_member_list_services(member_list: List):
        """
        导出会员信息service

        :param member_list: 会员信息列表
        :return: 会员信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'member_id': '会员编号',
            'member_name': '会员名称',
            'nick_name': '会员昵称',
            'email': '邮箱地址',
            'phonenumber': '手机号码',
            'gender': '会员性别',
            'birthday': '会员生日',
            'age': '会员年龄',
            'status': '状态',
            'create_by': '创建者',
            'create_at': '创建时间',
            'update_by': '更新者',
            'update_at': '更新时间',
            'remark': '备注',
        }

        data = member_list
        gender_mapping = {'0': '男', '1': '女', '2': '未知'}
        for item in data:
            item['gender'] = gender_mapping.get(item.get('gender'), '未知')
            item['status'] = '正常' if item.get('status') == '0' else '停用'

        new_data = [
            {mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in data
        ]
        binary_data = export_list2excel(new_data)

        return binary_data    
