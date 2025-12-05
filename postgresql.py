import asyncpg


class PostgreSQLClient:
    def __init__(self, **cfg):
        self.cfg = cfg

    async def connect(self):
        self.pool = await asyncpg.create_pool(**self.cfg)

    async def disconnect(self):
        assert self._pool is not None, "DatabaseBackend is not running"
        await self.pool.close()

    async def execute(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)


class DatabaseProxy:
    def __init__(self, db):
        self.db = db

    def saveOne(self, arg):
        pass

    def getOne(self, arg):
        pass
