
class Clasetotal:
    def firstn(self, n):
        num = 0
        while num < n:
            yield num
            num += 1

class Clase2:
    class Clase3:
        def firstn(self, n):
            num = n**2
            while num > n:
                yield num
                num -= 1


def primera():
    def segunda():
        def qsfn(n):
            #res = sum(Clasetotal.firstn(n))**2
            #print(res)
                num = 0
                while num < n:
                    yield num
                    num += 1

def generator():
    yield 'hola'


next(generator())

g = generator()
next(g)

#distintas formas de llamar un generator
#1º forma:

next(Clasetotal().firstn(5))

#2ª forma:


clase = Clasetotal()

next(clase.firstn(5))

#3ª forma:

clase = Clasetotal()

generator = clase.firstn(5)

next(generator)

#4ª forma

generator = Clasetotal().firstn(5)

next(generator)

##########################33
#formas de llamarlo usando un for

clase = Clasetotal()

for item in clase.firstn(5):
    print(item)


#probamos a hacer un call de la segunda

next(Clase2().Clase3().firstn(5))

nueva_clase = Clase2()

next(nueva_clase.Clase3().firstn(5))

nueva_clase3 = Clase2().Clase3().firstn(5)

next(nueva_clase3)


def f():
    return 'hola'

generator = f()

print(generator)





