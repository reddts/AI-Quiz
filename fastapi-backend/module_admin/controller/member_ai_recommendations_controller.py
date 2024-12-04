from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from services.member_ai_recommendations_service import MemberAIRecommendationService
from schemas.member_ai_recommendations_vo import CreateRecommendationVO, RecommendationVO
from database import get_db
from typing import List

# 初始化 router 实例
router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/", response_model=List[RecommendationVO])
async def get_all_recommendations(db: AsyncSession = Depends(get_db)):
    """
    获取所有用户AI建议记录
    :param db: 数据库会话
    :return: AI建议记录列表
    """
    return await MemberAIRecommendationService.get_all_recommendations(db)

@router.get("/{recommendation_id}", response_model=RecommendationVO)
async def get_recommendation_by_id(recommendation_id: int, db: AsyncSession = Depends(get_db)):
    """
    根据推荐ID获取单个推荐记录
    :param recommendation_id: 推荐记录ID
    :param db: 数据库会话
    :return: 推荐记录
    """
    return await MemberAIRecommendationService.get_recommendation_by_id(db, recommendation_id)

@router.post("/", response_model=RecommendationVO)
async def create_recommendation(recommendation: CreateRecommendationVO, db: AsyncSession = Depends(get_db)):
    """
    创建新的AI推荐记录
    :param recommendation: 新推荐记录数据
    :param db: 数据库会话
    :return: 创建的推荐记录
    """
    return await MemberAIRecommendationService.create_recommendation(db, recommendation)

@router.delete("/{recommendation_id}")
async def delete_recommendation(recommendation_id: int, db: AsyncSession = Depends(get_db)):
    """
    删除AI推荐记录
    :param recommendation_id: 推荐记录ID
    :param db: 数据库会话
    :return: 删除成功的提示信息
    """
    await MemberAIRecommendationService.delete_recommendation(db, recommendation_id)
    return {"detail": "Recommendation deleted successfully"}
