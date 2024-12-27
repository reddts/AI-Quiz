from datetime import datetime, time
from sqlalchemy import and_, delete, desc, func, or_, select, update
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

    @classmethod
    async def get_member_detail_by_id(cls, db: AsyncSession, member_id: int):
        """
        根据member_id获取会员详细信息

        :param db: orm对象
        :param member_id: 会员id
        :return: 当前member_id的会员信息对象
        """
        member_info = (await db.execute(select(Member).where(Member.del_flag == '0', Member.member_id == member_id).distinct())).scalars().first()
        
        return member_info

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
                Member.create_at.between(
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

    @classmethod
    async def get_member_by_info(cls, db: AsyncSession, member: MemberModel):
        """
        根据会员参数获取会员信息

        :param db: orm对象
        :param member: 会员参数
        :return: 当前会员参数的会员信息对象
        """
        query_member_info = (
            (
                await db.execute(
                    select(Member)
                    .where(
                        Member.del_flag == '0',
                        Member.member_name == member.member_name if member.member_name else True,
                        Member.phonenumber == member.phonenumber if member.phonenumber else True,
                        Member.email == member.email if member.email else True,
                    )
                    .order_by(desc(Member.create_at))
                    .distinct()
                )
            )
            .scalars()
            .first()
        )

        return query_member_info
    
    @classmethod
    async def add_member_dao(cls, db: AsyncSession, member: MemberModel):
        """
        新增用户数据库操作

        :param db: orm对象
        :param member: 用户对象
        :return: 新增校验结果
        """
        db_member = Member(**member.model_dump())
        db.add(db_member)
        await db.flush()

        return db_member
    

    @classmethod
    async def edit_member_dao(cls, db: AsyncSession, member: dict):
        """
        编辑会员数据库操作

        :param db: orm对象
        :param member: 需要更新的会员字典
        :return: 编辑校验结果
        """
        await db.execute(update(Member), [member])


    @classmethod
    async def delete_member_dao(cls, db: AsyncSession, member: MemberModel):
        """
        删除会员数据库操作

        :param db: orm对象
        :param member: 会员对象
        :return:
        """
        await db.execute(
            update(Member)
            .where(Member.member_id == member.member_id)
            .values(del_flag='2', update_by=member.update_by, update_at=member.update_at)
        )