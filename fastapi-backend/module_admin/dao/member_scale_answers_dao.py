from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.member_scale_answers import MemberScaleAnswer
from typing import Optional, List
from fastapi import HTTPException

class MemberScaleAnswerDAO:
    """
    数据访问对象（DAO）层，用于操作 `member_scale_answers` 表。
    提供了基本的 CRUD 操作与数据库交互方法。
    """

    @staticmethod
    async def get_answer_by_id(db: AsyncSession, answer_id: int) -> Optional[MemberScaleAnswer]:
        """
        根据回答ID获取量表回答记录
        :param db: 数据库会话
        :param answer_id: 回答记录ID
        :return: 量表回答记录或 None
        """
        result = await db.execute(select(MemberScaleAnswer).where(MemberScaleAnswer.answer_id == answer_id))
        answer = result.scalar_one_or_none()
        return answer

    @staticmethod
    async def get_all_answers(db: AsyncSession) -> List[MemberScaleAnswer]:
        """
        获取所有量表回答记录
        :param db: 数据库会话
        :return: 量表回答记录列表
        """
        result = await db.execute(select(MemberScaleAnswer))
        answers = result.scalars().all()
        return answers

    @staticmethod
    async def create_answer(db: AsyncSession, answer_data: dict) -> MemberScaleAnswer:
        """
        创建一条新的量表回答记录
        :param db: 数据库会话
        :param answer_data: 量表回答数据字典
        :return: 新创建的量表回答记录对象
        """
        new_answer = MemberScaleAnswer(**answer_data)
        db.add(new_answer)
        await db.commit()
        await db.refresh(new_answer)
        return new_answer

    @staticmethod
    async def delete_answer(db: AsyncSession, answer_id: int) -> bool:
        """
        删除量表回答记录
        :param db: 数据库会话
        :param answer_id: 回答记录ID
        :return: 是否删除成功
        """
        answer = await MemberScaleAnswerDAO.get_answer_by_id(db, answer_id)
        if not answer:
            raise HTTPException(status_code=404, detail="Answer not found")

        await db.delete(answer)
        await db.commit()
        return True
