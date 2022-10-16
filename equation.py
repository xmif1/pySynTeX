import ast
import inspect


def bind(string, **bindings):
    for left_symbol, right_symbol in bindings:
        string.replace(left_symbol, right_symbol)


class _equation:
    def __init__(self, func, bindings):
        self.bindings = bindings
        self.func = func
        self.ast = None

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def _set_ast(self):
        if ast is None:
            self.ast = ast.parse(inspect.getsource(self.func))

    def debug_print_bindings(self):
        print(self.bindings)


class equation:
    def __init__(self, **bindings):
        self.bindings = bindings

    def __call__(self, func):
        _arg_set = set(self.bindings.keys()).symmetric_difference(set(inspect.signature(func).parameters))

        if len(_arg_set) != 0:
            raise KeyError('Function argument names do not match equation bindings (missing: ' +
                           str(_arg_set).replace('{', '').replace('}', '') + ')')

        func = _equation(func, self.bindings)
        return func


@equation(n='n', init='a', ratio='r')  # Example showing how function parameters are bound to symbol representative
def geometric_progression(n, init, ratio):
    total = 0

    for i in range(n + 1):
        total += ratio ** i

    return init * total


geometric_progression.debug_print_bindings()


try:  # Example showing error reporting if bindings do not match
    @equation(a="\\alpha", b='\\beta')
    def binary_sum(b, c):
        return b + c
except KeyError as e:
    print(e)
