import aiofiles
import asyncio
import ijson


async def read_json_async(filename):
    f = await aiofiles.open(filename)
    async for json_item in ijson.items_async(f, "item"):
        yield json_item


async def main(fn):
    gen = read_json_async(fn)

    for _ in range(2):
        item = await anext(gen)
        print()
        print(item)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="A JSON file to parse.")

    args = parser.parse_args()
    # print(args.filename)

    asyncio.run(main(args.filename))
