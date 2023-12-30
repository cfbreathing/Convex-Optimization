from .function_wrap import unary_to_nary
from .utils import toposort


# Computation graph nodes
class Node():
    __slots__ = ['_value', '_children', '_parents',
                 '_gradient', '_serial_number']
    __array_priority__ = 100.0

    def __init__(self, value, parents, serial_number=-1):
        self._value = value
        self._parents = parents
        self._serial_number = serial_number
        self._children = []

    def __bool__(self):
        return bool(self._value)

    __nonzero__ = __bool__

    # Creates a new node at getitem, or returns if the node has already been created.
    def __getitem__(self, idx):
        children_idx = [child._serial_number for weight,
                        child in self._children]
        if idx not in children_idx:
            value = self._value[idx]
            parent = [self]
            serial_number = idx
            item = Node(value, parent, serial_number)
            self._serial_number = min(-idx-1, self._serial_number)
            self._children.append((1, item))
        else:
            item = self._children[children_idx.index(idx)][1]
        return item

    def __str__(self):
        return f"Node with value {str(self._value)}"

    def print_parents(self):
        for parent in self._parents:
            print("parent: ", parent)

    def print_children(self):
        for weight, child in self._children:
            print(f"child with {weight}: ", child)

    shape = property(lambda self: self._value.shape)
    ndim = property(lambda self: self._value.ndim)
    size = property(lambda self: self._value.size)
    dtype = property(lambda self: self._value.dtype)
    def __len__(self): return len(self._value)

    def __add__(self, other):
        if isinstance(other, Node):
            value = self._value + other._value
            result = Node(value, [self, other])
            self._children.append((1, result))
            other._children.append((1, result))
        else:
            value = self._value + other
            result = Node(value, [self])
            self._children.append((1, result))
        return result

    def __radd__(self, other):
        value = self._value + other
        result = Node(value, [self])
        self._children.append((1, result))

        return result

    def __sub__(self, other):
        if isinstance(other, Node):
            value = self._value - other._value
            result = Node(value, [self, other])
            self._children.append((1, result))
            other._children.append((-1, result))
        else:
            value = self._value - other
            result = Node(value, [self])
            self._children.append((1, result))

        return result

    def __rsub__(self, other):
        value = other - self._value
        result = Node(value, [self])
        self._children.append((-1, result))

        return result

    def __mul__(self, other):
        if isinstance(other, Node):
            value = self._value * other._value
            result = Node(value, [self, other])
            self._children.append((other._value, result))
            other._children.append((self._value, result))
        else:
            value = self._value * other
            result = Node(value, [self])
            self._children.append((other, result))

        return result

    def __rmul__(self, other):
        value = other * self._value
        result = Node(value, [self])
        self._children.append((other, result))
        return result

    def __truediv__(self, other):
        if isinstance(other, Node):
            value = self._value / other._value
            result = Node(value, [self, other])
            self._children.append((1./other._value, result))
            other._children.append((-(self._value/other._value**2), result))
        else:
            value = self._value / other
            result = Node(value, [self])
            self._children.append((1./other, result))

        return result

    def __rtruediv__(self, other):
        value = other / self._value
        result = Node(value, [self])
        self._children.append((-(other/self._value**2), result))
        return result

    def __pow__(self, other):
        assert isinstance(other, int), "Wrong pow!!!"
        value = self._value ** other
        result = Node(value, [self])
        self._children.append((other*self._value**(other-1), result))
        return result

    def backward(self):
        if self._children == []:
            self._gradient = [1]

        elif self._serial_number < -1:
            gradient = [None] * -self._serial_number
            for weight, child in self._children:
                gradient.__setitem__(child._serial_number, child._gradient[0])
            self._gradient = gradient

        else:
            self._gradient = [0]
            for weight, child in self._children:
                self._gradient[0] += weight * child._gradient[0]

    def get_gradient(self):
        return self._gradient


@unary_to_nary
def grad(fun, x):
    start_node = Node(x, None)
    end_node = fun(start_node)
    for node in toposort(end_node):
        node.backward()
    return start_node.get_gradient()
