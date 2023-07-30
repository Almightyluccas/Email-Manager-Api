import json
import inspect


class TestUtilities:

    def validate_json(self, json_str: str):
        self.do_nothing()
        try:
            json.loads(json_str)
            return True
        except json.JSONDecodeError:
            return False

    def get_all_methods(self, class_object: object):
        self.do_nothing()
        methods = inspect.getmembers(class_object, predicate=inspect.ismethod)
        method_names = [method[0] for method in methods]
        return method_names

    def parse_json_file(self, file_path: str):
        self.do_nothing()
        try:
            with open(file_path, 'r') as file:
                json_data = json.load(file)
            return json_data
        except FileNotFoundError:
            return f"File '{file_path}' not found"
        except json.JSONDecodeError:
            return f"Error decoding JSON data in file '{file_path}'"

    def do_nothing(self):
        pass
