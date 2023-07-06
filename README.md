# Installation
`pip install `

# Usage
## SELECT 
```python
from ksql-query-builder import Builder, SelectContainer
builder = Builder()

stream_name = "stream"
containers = [
    SelectContainer(column_name="value", path="value.power"),
    SelectContainer(column_name="time", path="value.time")
]
builder.build_select_query(stream_name, containers)
```

## CREATE STREAM
```python
from ksql-query-builder import Builder, CreateContainer
builder = Builder()

stream_name = "stream"
topic = "topic"
containers = [
    CreateContainer(path="value.time", type="STRING"),
    CreateContainer(path="value.power", type="DOUBLE")
    CreateContainer(path="id", type="STRING")
]
builder.build_create_stream_query(stream_name, topic, containers)
```