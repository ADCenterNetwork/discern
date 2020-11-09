
class Clase:
    def f(self):
        print('estamos en f')
        self.g()
    def g(self):
        print('estamos en g')


x = Clase()

print(x.f())