import re
# import ast
import inspect

from IPython.display import display, Latex


class _syntexObject:
    def __init__(self, tex):
        self._tex = tex

    def __str__(self):
        return self._tex

    def _repr_latex_(self):
        return '$' + self._tex + '$'

    def _ipython_display_(self):
        return display(Latex('$' + self._tex + '$'))


class _equation:
    def __init__(self, func, tex, bindings):
        self._bindings = bindings
        self._positionals = list(inspect.signature(func).parameters)
        self._tex = tex
        self._func = func
        # self._ast = None

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    # def _set_ast(self):
    #     if self._ast is None:
    #         self._ast = ast.parse(inspect.getsource(self._func))

    def _bind(self, *args, **kwargs):
        out = self._tex

        for k, v in enumerate(args):
            out = re.sub(r'\b' + self._bindings[self._positionals[k]] + r'\b', str(v), out)

        for k, v in kwargs.items():
            out = re.sub(r'\b' + self._bindings[k] + r'\b', str(v), out)

        return out

    def syntex(self, *args, **kwargs):
        return _syntexObject(self._bind(*args, **kwargs))

    def syntex_eval(self, res_str, *args, **kwargs):
        return _syntexObject(self._bind(*args, **kwargs) + res_str.format(str(self._func(*args, **kwargs))))


class equation:
    def __init__(self, tex, **kwargs):
        self.tex = tex
        self.bindings = kwargs

    def __call__(self, func):
        _arg_set = set(self.bindings.keys()).symmetric_difference(set(inspect.signature(func).parameters))

        if len(_arg_set) != 0:
            raise KeyError('Function argument names do not match equation bindings (missing: ' +
                           str(_arg_set).replace('{', '').replace('}', '') + ')')

        func = _equation(func, self.tex, self.bindings)
        return func
