import asyncio
from ixccontainer import IxcContainer
from query import read_json_async, query_JSON_data_and_create_container


def createIxcContainer(args=[]):
    return IxcContainer(*args)


async def main(fn):
    gen = read_json_async(fn)

    for _ in range(2):
        item = await anext(gen)
        args = query_JSON_data_and_create_container(item)
        container = createIxcContainer(args)
        print(container)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="A JSON file to parse.")

    args = parser.parse_args()
    # print(args.filename)

    asyncio.run(main(args.filename))
