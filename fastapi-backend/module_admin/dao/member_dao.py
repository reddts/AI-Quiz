from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.member import Member
from typing import Optional, List
from fastapi import HTTPException

class MemberDAO:
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

    @staticmethod
    async def get_all_members(db: AsyncSession) -> List[Member]:
        """
        获取所有用户信息
        :param db: 数据库会话
        :return: 用户列表
        """
        result = await db.execute(select(Member))
        members = result.scalars().all()
        return members

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
        member = await MemberDAO.get_member_by_id(db, user_id)
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
        member = await MemberDAO.get_member_by_id(db, user_id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        await db.delete(member)
        await db.commit()
        return True
