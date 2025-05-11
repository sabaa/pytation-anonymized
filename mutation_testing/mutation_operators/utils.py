import inspect


def get_defined_members(class_obj):
    members = inspect.getmembers(class_obj)
    defined_members = []
    for member in members:
        if member[0].startswith("__") and member[0].endswith("__"):
            continue
        defined_members.append(member)
    return defined_members


def get_members_with_class(members):
    member_source = {}
    for member in members:
        source = inspect._findclass(member[1])
        member_source[member[0]] = source
    return member_source


def find_shared_members(parents_data, child_dict, child_obj):

    inherited_methods = {}
    for method, source in child_dict.items():
        if source != child_obj:
            inherited_methods[method] = source
    shared_methods = []
    for method, source in inherited_methods.items():
        for parent, parent_dict in parents_data.items():
            for par_method, par_source in parent_dict.items():
                # if parent has the method
                if par_method == method:
                    shared_methods.append((method, parent, par_source))

    result = []
    for i in range(len(shared_methods)):
        method_i, parent_i, source_i = shared_methods[i]
        for j in range(i + 1, len(shared_methods)):
            method_j, parent_j, source_j = shared_methods[j]
            if method_i == method_j and source_i != source_j and parent_i != parent_j:
                result.append(method_i)
    return result


def get_shared_members(class_obj):
    parents_data = {}
    for parent in class_obj.__bases__:
        parent_dict = get_members_with_class(get_defined_members(parent))
        parents_data[parent] = parent_dict
    child_dict = get_members_with_class(get_defined_members(class_obj))
    return find_shared_members(parents_data, child_dict, class_obj)


def is_shared_methods_and_fields(class_obj):
    shared = get_shared_members(class_obj)
    if len(shared) > 0:
        return True
