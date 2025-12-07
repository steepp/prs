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
        self._db = db

    def _create_placeholder_str(self, args=[]):
        return ", ".join(f"${i + 1}" for i in range(len(args)))

    def _columns_str(self, args=[]):
        return ", ".join(f"{c}" for c in args)

    async def saveOne(self, data={}, tname="ixccontainers"):
        columns = self._columns_str(data.keys())
        values = data.values()
        placeholders = self._create_placeholder_str(values)
        query = f"INSERT INTO {tname} ({columns}) VALUES ({placeholders})"
        return await self._db.execute(query, *values)

    def getOne(self, arg):
        pass
