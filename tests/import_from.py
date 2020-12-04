#import generatorfind.generatorfind

#import ..generatorfind

from pruebas import Clase1_1, Clase2_1

#from import_test import import_test

#import import_test.import_test

from import_test import import_test_subfolder

#from import_test.import_test import Clase

#print(next(import_test.Clase().funcion()))

Clase1_1().Clase1_2().firstn(5)
Clase2_1().Clase2_2().firstn(5)


print(next(import_test_subfolder.test.Clase().funcion()))

'''
class Clase:
    def funcion(self):
        yield 'hola'

class Clase_grande:
    class Clase:
        def funcion(self):
            yield 'esto es otra funcion'

print(next(Clase().funcion()))
print(next(Clase_grande().Clase().funcion()))
'''

#from generatorfind.generatorfind import Code