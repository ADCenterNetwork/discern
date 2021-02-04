def generator(num):
    if num < 0:
        yield 'negativo'
    else:
        yield 'positivo'