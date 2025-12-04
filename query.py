import ijson
import jmespath
import aiofiles


async def read_json_async(filename):
    f = await aiofiles.open(filename)
    async for json_item in ijson.items_async(f, "item"):
        yield json_item


def query_json(q, json_object):
    return jmespath.search(q, json_object)


def query_JSON_data_and_create_container(json_object):
    res = []
    queries = [
        "name",
        "state.cpu.usage",
        "state.memory.usage",
        "created_at",
        "status",
        "state.network.* | [?addresses].addresses[].address",
    ]

    for q in queries:
        res.append(query_json(q, json_object))

    return res
