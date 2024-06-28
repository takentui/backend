import json


def producer_value_serializer(value: dict) -> bytes:
    return json.dumps(value).encode("utf-8")
