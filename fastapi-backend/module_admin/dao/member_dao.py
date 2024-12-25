from datetime import datetime, time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from module_admin.entity.do.member_do import Member
from typing import Optional, List
from module_admin.entity.vo.member_vo import (
    MemberModel,
    MemberPageQueryModel,
)
from utils.page_util import PageUtil

class MemberDao:
    """
    数据访问对象（DAO）层，用于操作 Member 表。
    提供了基本的 CRUD 操作与数据库交互方法。
    """

    @staticmethod
    async def get_member_by_id(db: AsyncSession, user_id: int) -> Optional[Member]:
        """
        根据用户ID获取用户信息
        :param db: 数据库会话
        :param user_id: 用户ID
        :return: 用户信息或 None
        """
        result = await db.execute(select(Member).where(Member.user_id == user_id))
        member = result.scalar_one_or_none()
        return member

    @classmethod
    async def get_member_list(
        cls, db: AsyncSession, query_object: MemberPageQueryModel,  is_page: bool = False
    ):
        """
        根据查询参数获取会员列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 会员列表信息对象
        """
        query = (
            select(Member)
            .where(
                Member.del_flag == '0',
                Member.member_id == query_object.member_id if query_object.member_id is not None else True,
                Member.member_name.like(f'%{query_object.member_name}%') if query_object.member_name else True,
                Member.nick_name.like(f'%{query_object.nick_name}%') if query_object.nick_name else True,
                Member.email.like(f'%{query_object.email}%') if query_object.email else True,
                Member.phonenumber.like(f'%{query_object.phonenumber}%') if query_object.phonenumber else True,
                Member.status == query_object.status if query_object.status else True,
                Member.gender == query_object.gender if query_object.gender else True,
                Member.created_at.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
                if query_object.begin_time and query_object.end_time
                else True,
            )           
            .order_by(Member.member_id)
            .distinct()
        )
        member_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return member_list

    @staticmethod
    async def create_member(db: AsyncSession, member_data: dict) -> Member:
        """
        创建一个新用户
        :param db: 数据库会话
        :param member_data: 用户数据字典
        :return: 新创建的用户对象
        """
        new_member = Member(**member_data)
        db.add(new_member)
        await db.commit()
        await db.refresh(new_member)
        return new_member

    @staticmethod
    async def update_member(db: AsyncSession, user_id: int, update_data: dict) -> Optional[Member]:
        """
        更新用户信息
        :param db: 数据库会话
        :param user_id: 用户ID
        :param update_data: 更新的数据字典
        :return: 更新后的用户对象
        """
        member = await MemberDao.get_member_by_id(db, user_id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        for key, value in update_data.items():
            setattr(member, key, value)

        await db.commit()
        await db.refresh(member)
        return member

    @staticmethod
    async def delete_member(db: AsyncSession, user_id: int) -> bool:
        """
        删除用户
        :param db: 数据库会话
        :param user_id: 用户ID
        :return: 是否删除成功
        """
        member = await MemberDao.get_member_by_id(db, user_id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        await db.delete(member)
        await db.commit()
        return True
