from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.keypool_do import Keypool
from module_admin.entity.vo.keypool_vo import KeypoolModel, KeypoolPageQueryModel
from utils.page_util import PageUtil


class KeypoolDao:
    """
    key池管理模块数据库操作层
    """

    @classmethod
    async def get_keypool_by_id(cls, db: AsyncSession, key_id: int):
        """
        根据key池id获取在用key池详细信息

        :param db: orm对象
        :param key_id: key池id
        :return: 在用key池信息对象
        """
        keypool_info = (
            (await db.execute(select(Keypool).where(Keypool.key_id == key_id, Keypool.status == '0')))
            .scalars()
            .first()
        )

        return keypool_info

    @classmethod
    async def get_keypool_detail_by_id(cls, db: AsyncSession, key_id: int):
        """
        根据key池id获取key池详细信息

        :param db: orm对象
        :param key_id: key池id
        :return: key池信息对象
        """
        keypool_info = (await db.execute(select(Keypool).where(Keypool.key_id == key_id))).scalars().first()

        return keypool_info

    @classmethod
    async def get_keypool_detail_by_info(cls, db: AsyncSession, keypool: KeypoolModel):
        """
        根据key池参数获取key池信息

        :param db: orm对象
        :param keypool: key池参数对象
        :return: key池信息对象
        """
        keypool_info = (
            (
                await db.execute(
                    select(Keypool).where(
                        Keypool.key_name == keypool.key_name if keypool.key_name else True,
                        Keypool.key_typeid == keypool.key_typeid if keypool.key_typeid else True,
                    )
                )
            )
            .scalars()
            .first()
        )

        return keypool_info

    @classmethod
    async def get_keypool_list(cls, db: AsyncSession, query_object: KeypoolPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取key池列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: key池列表信息对象
        """
        query = (
            select(Keypool)
            .where(
                Keypool.key_typeid == query_object.key_typeid if query_object.key_typeid else True,
                Keypool.key_name.like(f'%{query_object.key_name}%') if query_object.key_name else True,
                Keypool.status == query_object.status if query_object.status else True,
            )
            .order_by(Keypool.key_id)
            .distinct()
        )
        keypool_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return keypool_list

    @classmethod
    async def add_keypool_dao(cls, db: AsyncSession, keypool: KeypoolModel):
        """
        新增key池数据库操作

        :param db: orm对象
        :param keypool: key池对象
        :return:
        """
        db_keypool = Keypool(**keypool.model_dump())
        db.add(db_keypool)
        await db.flush()

        return db_keypool

    @classmethod
    async def edit_keypool_dao(cls, db: AsyncSession, keypool: dict):
        """
        编辑key池数据库操作

        :param db: orm对象
        :param keypool: 需要更新的key池字典
        :return:
        """
        await db.execute(update(Keypool), [keypool])

    @classmethod
    async def delete_keypool_dao(cls, db: AsyncSession, keypool: KeypoolModel):
        """
        删除key池数据库操作

        :param db: orm对象
        :param keypool: key池对象
        :return:
        """
        await db.execute(delete(Keypool).where(Keypool.key_id.in_([keypool.key_id])))

