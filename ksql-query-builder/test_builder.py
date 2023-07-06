import pytest

from builder import Builder
from container import CreateContainer, SelectContainer

def test_convert_path_to_select_form():
    b = Builder()
    path = "value.energy.total"
    expected_flattened_string = "value->energy->total"
    actual_flattened_string = b._convert_path_to_select_form(path)
    assert(expected_flattened_string == actual_flattened_string)

@pytest.mark.parametrize("paths, expected_column_string",[
    ([CreateContainer(path="power", type="DOUBLE"), CreateContainer(path="time", type="STRING")], "power DOUBLE, time STRING"),
    ([CreateContainer(path="value.energy", type="DOUBLE"), CreateContainer(path="value.time", type="STRING")], "value STRUCT<energy DOUBLE, time STRING>"),
    ([CreateContainer(path="value.energy", type="DOUBLE"), CreateContainer(path="test.time", type="STRING")], "test STRUCT<time STRING>, value STRUCT<energy DOUBLE>"),
    ([CreateContainer(path="value.power.total", type="DOUBLE"), CreateContainer(path="value.energy.time", type="STRING")], "value STRUCT<energy STRUCT<time STRING>, power STRUCT<total DOUBLE>>"),
    ([CreateContainer(path="value.power.total", type="DOUBLE"), CreateContainer(path="value.power.time", type="STRING"), CreateContainer(path="test", type="DOUBLE")], "test DOUBLE, value STRUCT<power STRUCT<time STRING, total DOUBLE>>")
])
def test_column_string(paths, expected_column_string):
    b = Builder()
    actual_column_string = b._build_column_string(paths)
    assert(expected_column_string == actual_column_string)

@pytest.mark.parametrize("stream_name, containers, expected_query",[
    ("stream1", [SelectContainer(path="power", column_name="power"), SelectContainer(path="time", column_name="time")], "SELECT power as power, time as time FROM stream1"),
    ("stream1", [SelectContainer(path="value.power", column_name="power"), SelectContainer(path="value.time", column_name="time")], "SELECT value->power as power, value->time as time FROM stream1"),
])
def test_build_select_query(stream_name, containers, expected_query):
    b = Builder()
    actual_query = b.build_select_query(stream_name, containers)
    assert(expected_query == actual_query)

@pytest.mark.parametrize("stream_name, topic, containers, expected_query",[
    ("stream1", 'topic', [CreateContainer(path="power", type="DOUBLE"), CreateContainer(path="time", type="STRING")], "CREATE STREAM stream1 (power DOUBLE, time DOUBLE) WITH (kafka_topic='topic', value_format='json', partitions=1)"),
    ("stream1", 'topic', [CreateContainer(path="value.power", type="DOUBLE"), CreateContainer(path="value.time", type="STRING")], "CREATE STREAM stream1 (value STRUCT<power DOUBLE, time STRING>) WITH (kafka_topic='topic', value_format='json', partitions=1)"),
])
def test_build_create_stream_query(stream_name, topic, containers, expected_query):
    b = Builder()
    actual_query = b.build_create_stream_query(stream_name, topic, containers)
    assert(expected_query == actual_query)