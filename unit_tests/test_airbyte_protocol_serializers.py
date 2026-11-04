# Copyright (c) 2026 Airbyte, Inc., all rights reserved.

from copy import deepcopy

import orjson
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
        {"present": "value"},
        {
            "nullable": None,
            "nested": {"x": None},
            "items": [None, {"y": None}],
            "empty_object": {},
            "empty_list": [],
            "false": False,
            "zero": 0,
            "empty_string": "",
        },
    ],
)
def test_record_data_preserves_null_and_missing_fields(data):
    original_data = deepcopy(data)
    message = AirbyteMessage(
        type=Type.RECORD,
        record=AirbyteRecordMessage(stream="example", data=data, emitted_at=1),
    )

    wire = orjson.loads(orjson.dumps(AirbyteMessageSerializer.dump(message)))

    assert wire == {
        "type": "RECORD",
        "record": {"stream": "example", "data": original_data, "emitted_at": 1},
    }
    assert "missing" not in wire["record"]["data"]
    assert ("nullable" in wire["record"]["data"]) == ("nullable" in original_data)
    assert data == original_data
    assert AirbyteMessageSerializer.load(wire) == message


def test_record_optional_envelope_fields_are_preserved_when_set():
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
