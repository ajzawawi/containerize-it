from jinja2 import Environment, StrictUndefined
from containerize.transformer.filters.ansible_filters import get_filters
from ansible.plugins.filter.core import FilterModule as CoreFilterModule
from ansible.plugins.filter.mathstuff import FilterModule as MathFilterModule
from containerize.transformer.filters.registry import get_filters

class FilterRegistry:
    def __init__(self):
        self.env = Environment(undefined=StrictUndefined)
        self._register_builtin_filters()

    def _register_builtin_filters(self):
        # We're just using the default ansible filters here
        core_filters = CoreFilterModule().filters()
        self.env.filters.update(core_filters)
        
        math_filters = MathFilterModule().filters()
        self.env.filters.update(math_filters)

        # Order matters, this way we can override any default ansible filters with 
        # a custom implementation if needed. Some ansible filters will need
        # to be modified for the use case (like the ones returning generators)
        custom_filters = get_filters()
        self.env.filters.update(custom_filters)        

    def get_env(self):
        return self.env
