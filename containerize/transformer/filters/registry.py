from jinja2 import Environment, StrictUndefined
from containerize.transformer.filters.ansible_filters import get_filters

class FilterRegistry:
    def __init__(self):
        self.env = Environment(undefined=StrictUndefined)
        self._register_builtin_filters()

    def _register_builtin_filters(self):
        for name, func in get_filters().items():
            self.env.filters[name] = func

    def get_env(self):
        return self.env
