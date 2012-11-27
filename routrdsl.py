"""

    routrdsl -- DSL for defining routes for routr from a docstring
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import re
import routr
import routrschema

__all__ = ('parse',)

def parse(input, namespace):
    routes = []

    for line in input.split('\n'):
        line = line.strip()
        if not is_route(line):
            continue
        method, path = method_split_re.split(line, 1)
        method = routr.HTTPMethod(method)
        guards = []
        if '?' in path:
            path, qs = path.split('?', 1)
            guards.append(compile_qs(qs))

        args = [method, path] + guards + [ref_target(method, path, namespace)]
        routes.append(routr.route(*args))

    return routr.route(*routes) if routes else None

method_split_re = re.compile(' +')
is_route = re.compile('^(GET|POST|PUT|DELETE|PATCH|OPTIONS|TRACE) +').search
validators = {'str': str, 'int': int, 'bool': bool}
is_field_optional = re.compile(r'^\[.+\]$').search
strip_path_re1 = re.compile('{[a-zA-Z0-9]+(:[a-zA-Z0-9]+)?}')
strip_path_re2 = re.compile('/+')

def ref_target(method, path, namespace):
    path = strip_path_re1.sub('', path)
    path = strip_path_re2.sub('/', path)
    path = path.replace('/', '_')
    if path.startswith('_'):
        path = path[1:]
    if path.endswith('_'):
        path = path[:-1]
    path = method.lower() + '_' + path
    return namespace[path]

def compile_qs(line):
    items = line.split('&')
    fields = {}
    for item in items:
        if is_field_optional(item):
            mod = routrschema.opt
            item = item[1:-1]
        else:
            mod = lambda x: x
        if '=' in item:
            name, validator = item.split('=', 1)
            fields[name] = mod(validators[validator])
        else:
            fields[name] = mod(bool)
    return routrschema.qs(**fields)
