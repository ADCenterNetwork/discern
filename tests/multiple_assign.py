class Clase:
    def f(self):
        yield 'sdhfkldsj'

class Clase2:
    def g(self):
        yield 'hola'

a, b = Clase().f(), Clase2().g()

next(a)

next(b)