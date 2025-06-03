from containerize.transformer.filters.registry import FilterRegistry

def get_rendered(template_str, **context):
    env = FilterRegistry().get_env()
    template = env.from_string(template_str)
    return template.render(**context)


def test_flatten_filter():
    output = get_rendered("{{ value | flatten }}", value=[[1, 2], [3, 4], 5])
    assert output == "[1, 2, 3, 4, 5]"


def test_combine_filter():
    output = get_rendered("{{ value1 | combine(value2) }}", value1={"a": 1}, value2={"b": 2})
    assert output == "{'a': 1, 'b': 2}"


def test_dict2items_filter():
    output = get_rendered("{{ value | dict2items }}", value={"foo": "bar", "baz": "qux"})
    assert "'key': 'foo'" in output
    assert "'value': 'bar'" in output
    assert "'key': 'baz'" in output
    assert "'value': 'qux'" in output
