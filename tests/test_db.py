import pytest
from testcontainers.postgres import PostgresContainer
from postgresql import PostgreSQLClient


@pytest.fixture(scope="module", autouse=True)
def postgres():
    postgres = PostgresContainer(
        image="postgres:latest",
        username="testuser",
        password="testpass",
        dbname="testdb",
        port=5432,
    )
    postgres.start()
    yield postgres
    postgres.stop()


@pytest.fixture(scope="module")
async def db_proxy(postgres: PostgresContainer):
    client = PostgreSQLClient(postgres.get_connection_url())

    await client.connect()

    await client.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT
        )
        """
    )
    yield client

    await client.execute("DROP TABLE IF EXISTS users")
    await client.disconnect()


@pytest.mark.asyncio
async def test_users_table_exists(db_proxy):
    rows = await db_proxy.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_name = 'users'
    """)

    assert len(rows) == 1
    assert rows[0]["table_name"] == "users"
