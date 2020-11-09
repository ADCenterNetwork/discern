import math

class algo():
    def       funcion(self, a,b):
        if b != 0:
            yield float(a)/b
        else:
            yield 'unable to do this operation'

clase = algo()

g = clase.funcion(10,5)
f = clase.funcion(10,0)

print(next(g))
print(next(f))