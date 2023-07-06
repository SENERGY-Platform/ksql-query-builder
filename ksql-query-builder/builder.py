from collections import defaultdict
from container import CreateContainer

class Builder():
    def __init__(self) -> None:
        pass

    def _convert_path_to_select_form(self, access_path):
        string = ""
        access_paths = access_path.split('.')
        for i, level in enumerate(access_paths):
            string += level

            if i < len(access_paths)-1:
                string += '->'
        return string

    def _build_select_string(self, select_containers):
        string = ""
        number_containers = len(select_containers)

        for i, select_container in enumerate(select_containers):
            flattened_path = self._convert_path_to_select_form(select_container.path)
            string += f"{flattened_path} as {select_container.column_name}"

            if i < number_containers - 1:
                string += ", "

        return string

    def build_select_query(self, stream_name, select_containers):
        select_string = self._build_select_string(select_containers)
        query = f"""SELECT {select_string} FROM {stream_name}"""
        return query

    def _build_column_string(self, create_containers):
        string = ""
        
        first_container_to_rest = defaultdict(lambda: [])

        for container in create_containers:
            print(container)
            path = container.path.split('.')
            first_path = path[0]
            rest_paths = path[1:]

            first_container = CreateContainer(path=first_path, type=container.type)
            if rest_paths:
                next_container = CreateContainer(path=".".join(rest_paths), type=container.type)
                first_container_to_rest[first_container].append(next_container) 
            else:
                first_container_to_rest[first_container] = []
                

        all_first_containers = sorted(first_container_to_rest.keys())
        number_of_groups = len(all_first_containers)

        for i, first_container in enumerate(all_first_containers):
            next_containers = first_container_to_rest[first_container]
            first_path = first_container.path

            if not next_containers:
                string += f'{first_path} {first_container.type}'
            else:
                string += f'{first_path} STRUCT<'
                string += self._build_column_string(next_containers)
                string += '>'
          
            if len(create_containers) > 1 and i < number_of_groups-1:
                string += ', '

        return string

    def build_create_stream_query(self, stream, topic, create_containers):
        value_string = self._build_column_string(create_containers)
        query = f"""CREATE STREAM {stream} ({value_string}) WITH (kafka_topic='{topic}', value_format='json', partitions=1)"""
        return query

 
