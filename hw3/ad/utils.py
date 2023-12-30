import operator


# Used to replace parameters, pass closures
def subvals(x, ivs):
    x_ = list(x)
    for i, v in ivs:
        x_[i] = v
    return tuple(x_)


# For topological sorting
def toposort(end_node, parents=operator.attrgetter('_parents')):
    child_counts = {}
    stack = [end_node]
    while stack:
        node = stack.pop()
        if node in child_counts:
            child_counts[node] += 1
        else:
            child_counts[node] = 1
            if parents(node) is not None:
                stack.extend(parents(node))

    childless_nodes = [end_node]
    while childless_nodes:
        node = childless_nodes.pop()
        yield node
        if parents(node) is not None:
            for parent in parents(node):
                if child_counts[parent] == 1:
                    childless_nodes.append(parent)
                else:
                    child_counts[parent] -= 1