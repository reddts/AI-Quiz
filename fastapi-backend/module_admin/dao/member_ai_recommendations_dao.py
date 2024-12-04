from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.member_ai_recommendations import MemberAIRecommendation
from typing import Optional, List
from fastapi import HTTPException

class MemberAIRecommendationDAO:
    """
    数据访问对象（DAO）层，用于操作 `member_ai_recommendations` 表。
    提供了基本的 CRUD 操作与数据库交互方法。
    """

    @staticmethod
    async def get_recommendation_by_id(db: AsyncSession, recommendation_id: int) -> Optional[MemberAIRecommendation]:
        """
        根据建议ID获取建议记录
        :param db: 数据库会话
        :param recommendation_id: 建议记录ID
        :return: 建议记录或 None
        """
        result = await db.execute(select(MemberAIRecommendation).where(MemberAIRecommendation.recommendation_id == recommendation_id))
        recommendation = result.scalar_one_or_none()
        return recommendation

    @staticmethod
    async def get_all_recommendations(db: AsyncSession) -> List[MemberAIRecommendation]:
        """
        获取所有AI建议记录
        :param db: 数据库会话
        :return: AI建议记录列表
        """
        result = await db.execute(select(MemberAIRecommendation))
        recommendations = result.scalars().all()
        return recommendations

    @staticmethod
    async def create_recommendation(db: AsyncSession, recommendation_data: dict) -> MemberAIRecommendation:
        """
        创建一条新的建议记录
        :param db: 数据库会话
        :param recommendation_data: 建议记录数据字典
        :return: 新创建的建议记录对象
        """
        new_recommendation = MemberAIRecommendation(**recommendation_data)
        db.add(new_recommendation)
        await db.commit()
        await db.refresh(new_recommendation)
        return new_recommendation

    @staticmethod
    async def delete_recommendation(db: AsyncSession, recommendation_id: int) -> bool:
        """
        删除建议记录
        :param db: 数据库会话
        :param recommendation_id: 建议记录ID
        :return: 是否删除成功
        """
        recommendation = await MemberAIRecommendationDAO.get_recommendation_by_id(db, recommendation_id)
        if not recommendation:
            raise HTTPException(status_code=404, detail="Recommendation not found")

        await db.delete(recommendation)
        await db.commit()
        return True
