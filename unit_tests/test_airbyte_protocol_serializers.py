# Copyright (c) 2026 Airbyte, Inc., all rights reserved.

import json

import pytest

from airbyte_cdk.models import (
    AirbyteMessage,
    AirbyteMessageSerializer,
    AirbyteRecordMessage,
    Type,
)


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"nullable": None},
        {
            "nullable": None,
            "nested": {"x": None},
            "items": [None, {"y": None}],
            "empty_object": {},
            "empty_array": [],
            "false": False,
            "zero": 0,
            "empty_string": "",
        },
    ],
)
def test_record_serialization_preserves_payload(data):
    message = AirbyteMessage(
        type=Type.RECORD,
        record=AirbyteRecordMessage(stream="example", data=data, emitted_at=1),
    )

    wire = json.loads(json.dumps(AirbyteMessageSerializer.dump(message)))

    assert wire == {
        "type": "RECORD",
        "record": {"stream": "example", "data": data, "emitted_at": 1},
    }
    assert "missing" not in wire["record"]["data"]
    assert AirbyteMessageSerializer.load(wire) == message


def test_record_serialization_preserves_namespace():
    message = AirbyteMessage(
        type=Type.RECORD,
        record=AirbyteRecordMessage(
            stream="example", namespace="public", data={"nullable": None}, emitted_at=1
        ),
    )

    wire = AirbyteMessageSerializer.dump(message)

    assert wire == {
        "type": "RECORD",
        "record": {
            "stream": "example",
            "namespace": "public",
            "data": {"nullable": None},
            "emitted_at": 1,
        },
    }
    assert AirbyteMessageSerializer.load(wire) == message
