import logging
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Union
from exceptions.exception import ServiceException
from module_admin.dao.member_dao import MemberDao
from module_admin.entity.vo.member_vo import (
    CreateMemberModel,
    EditMemberModel,
    MemberModel,
    MemberPageQueryModel,
    MemberInfoModel,
    DeleteMemberModel,
    )
from config.constant import CommonConstant
from module_admin.entity.vo.common_vo import CrudResponseModel
from utils.page_util import PageResponseModel
from utils.common_util import SqlalchemyUtil

logger = logging.getLogger(__name__)  # 日志记录器

class MemberService:
    """
    Member 服务层，提供业务逻辑处理功能
    """

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


    @classmethod
    async def edit_member_services(cls, query_db: AsyncSession, page_object: EditMemberModel):
        """
        编辑会员信息service

        :param query_db: orm对象
        :param page_object: 编辑会员对象
        :return: 编辑会员校验结果
        """
        edit_member = page_object.model_dump()
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

