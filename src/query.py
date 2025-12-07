import ijson
import jmespath
import aiofiles


async def read_json_async(filename):
    f = await aiofiles.open(filename)
    async for json_item in ijson.items_async(f, "item"):
        yield json_item
    await f.close()


def parse_json(q, json_object):
    return jmespath.search(q, json_object)


def init_parser(queries):
    def query_json(json_object):
        res = []
        for q in queries:
            res.append(parse_json(q, json_object))
        return res

    return query_json
