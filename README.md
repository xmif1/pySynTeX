# The ```pySynTeX``` Package

With it's beginner-friendly syntax and extensive package ecosystem, the Python programming language has proved useful to many scientists across a number of fields. 

The ```pySynTeX``` package is intended as a documentation tool for these scientists, by providing function decorators that allow for symbolic binding between a textual representation in LaTeX and the parameters of a function. This is best illustrated by an example, which also exemplifies how simple using ```pySynTeX``` is.

```
@equation("\sum\limits_{i = 0}^{n} a \cdot r^i", n="n", init="a", ratio="r")
def geometric_progression(n, init, ratio):
    total = 0

    for i in range(n+1):
        total += ratio**i

    return init*total
```

There are a number of observations we can make straight away. Firstly, the first argument of the decorator is a string written in LaTeX syntax which represents in mathematical notation the equation of a geometric progression. Secondly, observe that the subsequent arguments _bind_ a paramater of the function to the corresponding _symbol_ in the LaTeX string. This binding allows for the substitution of symbols with numbers. For example,

```
geometric_progression.syntex(9, 1, 1)
```
results in the output
```
"\sum\limits_{i = 0}^{9} 1 \cdot 1^i"
```

Observe how ```geometric_progression``` is no longer simply a function, but is rather an extended callable object, by virtue of the ```@equation``` decorator.

We can even include the result of the function for a given set of parameter values, by using Python-style formatted strings. For example,
```
geometric_progression.syntex_eval(" = {}", 9, 1, 1)
```
results in the output
```
"\sum\limits_{i = 0}^{9} 1 \cdot 1^i = 10"
```

In contrast to existing solutions, ```pySynTeX``` requires no modification to existing code, besides the addition of a simple decorator.