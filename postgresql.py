import asyncpg


class PostgreSQLClient:
    def __init__(self, dsn):
        self.cfg = dsn

    async def connect(self):
        self._pool = await asyncpg.create_pool(self.cfg)

    async def disconnect(self):
        assert self._pool is not None, "DatabaseBackend is not running"
        await self._pool.close()

    async def fetch(self, query: str, *args):
        async with self._pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def execute(self, query: str, *args):
        async with self._pool.acquire() as conn:
            return await conn.execute(query, *args)


class DatabaseProxy:
    def __init__(self, db):
        self.db = db

    def saveOne(self, arg):
        pass

    def getOne(self, arg):
        pass
