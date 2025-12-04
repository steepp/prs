from dataclasses import dataclass
from datetime import date
import aiofiles
import asyncio
import ijson
import jmespath


async def read_json_async(filename):
    f = await aiofiles.open(filename)
    async for json_item in ijson.items_async(f, "item"):
        yield json_item


@dataclass
class IxcContainer:
    name: str
    cpu_usage: int
    memory_usage: int
    created_at: date
    status: str
    ip_addresses: list


def query_json(q, json_object):
    return jmespath.search(q, json_object)


def query_JSON_data_and_create_container(json_object):
    args = []
    queries = [
        "name",
        "state.cpu.usage",
        "state.memory.usage",
        "created_at",
        "status",
        "state.network.*.hwaddr",
    ]

    for q in queries:
        args.append(query_json(q, json_object))

    container = IxcContainer(*args)
    print(container)


async def main(fn):
    gen = read_json_async(fn)

    for _ in range(2):
        item = await anext(gen)
        query_JSON_data_and_create_container(item)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="A JSON file to parse.")

    args = parser.parse_args()
    # print(args.filename)

    asyncio.run(main(args.filename))
