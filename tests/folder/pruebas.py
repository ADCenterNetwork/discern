#NO MODIFICAR CÓDIGO, O SE ARRUINAN LOS TESTS
#MODIFICAR SOLO DEL FINAL HACIA ABAJO

class Clase1_1:
    class Clase1_2:
        def firstn(self, n):
            num = 0
            while num < n:
                yield num
                num += 1
    class Clase1_3:
        def firstn(self, n):
            num = 0
            while num < n:
                yield num
                num += 1

class Clase2_1:
    class Clase2_2:
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

next(Clase1_1().Clase1_2().firstn(5))

#2ª forma:


clase = Clase1_1().Clase1_2()

next(clase.firstn(5))

#3ª forma:

clase = Clase1_1().Clase1_3()

generator = clase.firstn(5)

next(generator)

#4ª forma

generator = Clase1_1().Clase1_2().firstn(5)

next(generator)

##########################33
#formas de llamarlo usando un for

clase = Clase1_1().Clase1_2()

for item in clase.firstn(5):
    print(item)


#probamos a hacer un call de la segunda

asignacion1 = Clase2_1()

next(asignacion1.Clase2_2().firstn(5))

asignacion2_1 = Clase2_1()
asignacion2_2 = asignacion2_1.Clase2_2()
next(asignacion2_2.firstn(5))

asignacion3_1 = Clase2_1().Clase2_2()
asignacion3_2 = asignacion3_1.firstn(5)
next(asignacion3_2)




