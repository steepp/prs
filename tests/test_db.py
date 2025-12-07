import pytest
from postgresql import PostgreSQLClient, DatabaseProxy


@pytest.fixture()
async def db_pool():
    dsn = "postgresql://testuser:password@localhost:53140/testdb"

    client = PostgreSQLClient(dsn)

    await client.connect()

    yield client

    await client.disconnect()


@pytest.mark.asyncio
async def test_db_connection_established(db_pool):
    await db_pool.execute(
        """
        CREATE TABLE IF NOT EXISTS names (
              id serial PRIMARY KEY,
              name VARCHAR (255) NOT NULL)
        """
    )

    rows = await db_pool.fetch("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_name = 'names'
    """)

    assert len(rows) == 1
    assert rows[0]["table_name"] == "names"

    await db_pool.execute("DROP TABLE IF EXISTS names")


@pytest.mark.asyncio
async def test_saveOne(db_pool):
    dproxy = DatabaseProxy(db_pool)

    await db_pool.execute(
        """
        CREATE TABLE IF NOT EXISTS names (
              id serial PRIMARY KEY,
              name VARCHAR (255) NOT NULL)
        """
    )

    res = await dproxy.saveOne({"name": "testname"}, "names")

    number_of_rows_inserted = int(res.split(" ")[2])

    assert number_of_rows_inserted == 1

    await db_pool.execute("DROP TABLE IF EXISTS names")
