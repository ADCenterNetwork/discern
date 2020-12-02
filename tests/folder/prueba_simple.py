class Clase1:
    class Clase2:
        def f(self):
            yield 'hola'


next(Clase1().Clase2().f())

class Clase:
    pass

def f():
    yield 'hola'

Clase()

x = Clase()

g = f()
next(g)
next(f())