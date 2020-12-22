class Clase1():
    def funcion(self):
        yield 'hola'
class Clase2():
    def funcion(self):
        return 'hola'

correct = Clase1().funcion()
correct2 = correct
next(correct2)
#si hago correct2 = correct() no lo detecta como assign pero aparece en calls la linea 9
incorrect = Clase2().funcion()
next(incorrect)