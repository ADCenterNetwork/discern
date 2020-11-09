

class x():
    def g():
        def f(self):
            yield 'hola'

generators = [['x', 'g', 'f']]

def generator_find(i):
    try:
        if generators[i] == called:
            for child in item.iter_child_nodes:
                if generators[i+1] == called:
                    generator_find(i+1)
    except IndexError:
        return 


generators[0]

    

x().g().f()



# 1ª posibilidad
generator = x().f()

print(next(generator))

#2ª posibilidad
clase = x()

generator = clase.f()

print(next(generator))

#3ª posibilidad

print(next(x().f()))



