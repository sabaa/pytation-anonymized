from importlib import import_module


def get_module_from_path(path):
    module_name = path.replace('/', '.')
    module_name = module_name.removesuffix('.py')
    return import_module(module_name)
