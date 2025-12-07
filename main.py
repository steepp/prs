import os
import asyncio
from contextlib import asynccontextmanager

from src.ixccontainer import IxcContainer
from src.query import read_json_async, init_parser
from src.postgresql import PostgreSQLClient, DatabaseProxy

from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def setup_database():
    host = os.getenv("DBHOST", "localhost")
    port = os.getenv("DBPORT", "5432")
    username = os.getenv("DBUSER", "postgres")
    password = os.getenv("DBPASSWORD", "postgres")
    database = os.getenv("DBNAME", "postgres")

    dsn = f"postgresql://{username}:{password}@{host}:{port}/{database}"

    dbclient = PostgreSQLClient(dsn)
    await dbclient.connect()
    yield dbclient
    await dbclient.disconnect()


async def setup_table(client):
    containers_table_table = """
        CREATE TABLE IF NOT EXISTS ixccontainers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            cpu_usage INTEGER NOT NULL,
            memory_usage INTEGER NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(50) NOT NULL,
            ip_addresses TEXT[] NOT NULL
        )
        """

    await client.execute(containers_table_table)


def createIxcContainer(args=[]):
    return IxcContainer(*args)


async def main(fn):
    gen = read_json_async(fn)

    queries = [
        "name",
        "state.cpu.usage",
        "state.memory.usage",
        "created_at",
        "status",
        "state.network.* | [?addresses].addresses[].address",
    ]

    parse = init_parser(queries)

    async with setup_database() as db:
        await setup_table(db)

        dbproxy = DatabaseProxy(db)

        # async for item in gen:
        item = await anext(gen)
        args = parse(item)

        container = createIxcContainer(args)
        print(container.name)

        await dbproxy.saveOne(container)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="A JSON file to parse.")

    args = parser.parse_args()
    # print(args.filename)

    asyncio.run(main(args.filename))
