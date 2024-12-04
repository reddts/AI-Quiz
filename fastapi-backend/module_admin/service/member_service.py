import logging
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from exceptions.exception import ServiceException
from dao.member_dao import MemberDao
from schemas.member_vo import CreateMemberVO, UpdateMemberVO, MemberVO
from config.constant import CommonConstant
from utils.common_util import SqlalchemyUtil, Pagination

logger = logging.getLogger(__name__)  # 日志记录器

class MemberService:
    """
    Member 服务层，提供业务逻辑处理功能
    """

    @classmethod
    async def get_all_members(cls, db: AsyncSession, page: Optional[int] = None, size: Optional[int] = None):
        """
        获取所有会员信息（支持分页）

        :param db: 数据库会话
        :param page: 当前页码
        :param size: 每页大小
        :return: 分页或全部会员信息的列表
        """
        try:
            logger.info(f"Fetching member list with page={page}, size={size}")
            
            members = await MemberDao.get_all_members(db)
            member_list = [MemberVO(**SqlalchemyUtil.serialize_result(member)) for member in members]
            
            # 支持分页
            if page and size:
                paginated_result = Pagination.paginate(member_list, page, size)
                return paginated_result
            return member_list
        except Exception as e:
            logger.error("Failed to fetch member list", exc_info=True)
            raise ServiceException(message="获取会员列表失败", details=str(e))

    @classmethod
    async def get_member_by_id(cls, db: AsyncSession, user_id: int, redis):
        """
        根据用户ID获取单个会员信息（支持Redis缓存）

        :param db: 数据库会话
        :param user_id: 用户ID
        :param redis: Redis 客户端
        :return: 单个会员信息
        """
        try:
            cache_key = f"member:{user_id}"
            cached_member = await redis.get(cache_key)
            if cached_member:
                logger.info(f"Cache hit for member ID: {user_id}")
                return MemberVO(**SqlalchemyUtil.deserialize_json(cached_member))

            logger.info(f"Cache miss for member ID: {user_id}")
            member = await MemberDao.get_member_by_id(db, user_id)
            if not member:
                raise ServiceException(message=f"用户ID为 {user_id} 的会员信息不存在")

            member_vo = MemberVO(**SqlalchemyUtil.serialize_result(member))
            # 缓存数据
            await redis.set(cache_key, SqlalchemyUtil.serialize_json(member_vo), ex=3600)
            return member_vo
        except Exception as e:
            logger.error(f"Failed to fetch member by ID: {user_id}", exc_info=True)
            raise ServiceException(message="获取会员信息失败", details=str(e))

    @classmethod
    async def create_member(cls, request: Request, db: AsyncSession, member_vo: CreateMemberVO, redis):
        """
        创建新会员（清理相关缓存）

        :param request: 请求对象
        :param db: 数据库会话
        :param member_vo: 创建会员的数据对象
        :param redis: Redis 客户端
        :return: 创建的会员信息
        """
        try:
            existing_member = await MemberDao.get_member_by_username(db, member_vo.username)
            if existing_member:
                raise ServiceException(message=f"用户名 {member_vo.username} 已存在")
            
            new_member = await MemberDao.create_member(db, member_vo)
            await db.commit()

            # 清理相关缓存
            await redis.delete("member:all")
            return MemberVO(**SqlalchemyUtil.serialize_result(new_member))
        except Exception as e:
            logger.error("Failed to create member", exc_info=True)
            await db.rollback()
            raise ServiceException(message="创建会员失败", details=str(e))

    @classmethod
    async def update_member(cls, request: Request, db: AsyncSession, user_id: int, member_vo: UpdateMemberVO, redis):
        """
        更新会员信息（清理相关缓存）

        :param request: 请求对象
        :param db: 数据库会话
        :param user_id: 用户ID
        :param member_vo: 更新的会员数据对象
        :param redis: Redis 客户端
        :return: 更新后的会员信息
        """
        try:
            existing_member = await MemberDao.get_member_by_id(db, user_id)
            if not existing_member:
                raise ServiceException(message=f"用户ID为 {user_id} 的会员信息不存在")

            updated_member = await MemberDao.update_member(db, user_id, member_vo)
            await db.commit()

            # 清理相关缓存
            await redis.delete(f"member:{user_id}")
            await redis.delete("member:all")
            return MemberVO(**SqlalchemyUtil.serialize_result(updated_member))
        except Exception as e:
            logger.error(f"Failed to update member ID: {user_id}", exc_info=True)
            await db.rollback()
            raise ServiceException(message="更新会员失败", details=str(e))

    @classmethod
    async def delete_member(cls, request: Request, db: AsyncSession, user_id: int, redis):
        """
        删除会员信息（清理相关缓存）

        :param request: 请求对象
        :param db: 数据库会话
        :param user_id: 用户ID
        :param redis: Redis 客户端
        :return: 删除成功的信息
        """
        try:
            existing_member = await MemberDao.get_member_by_id(db, user_id)
            if not existing_member:
                raise ServiceException(message=f"用户ID为 {user_id} 的会员信息不存在")
            
            await MemberDao.delete_member(db, user_id)
            await db.commit()

            # 清理相关缓存
            await redis.delete(f"member:{user_id}")
            await redis.delete("member:all")
            return {"detail": f"用户ID为 {user_id} 的会员信息已删除"}
        except Exception as e:
            logger.error(f"Failed to delete member ID: {user_id}", exc_info=True)
            await db.rollback()
            raise ServiceException(message="删除会员失败", details=str(e))

