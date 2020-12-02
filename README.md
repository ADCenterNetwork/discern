# Generatorfind

## What it does

This program will read a file as input, and it will look for all the instances that every single generator function is called. 

The output that we will receive is a dictionary, in which the keys are the names of all of our generators in our program, and the values of these keys are lists with numbers, representing the lines of our program in which these generators were called.

In short, this program is aimed to find all of the callsites of generators in a program.

So, for instance, if we have the following code:

```python
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

generator = Clase1_1().Clase1_2().firstn(5) #line 37
next(generator) #line 38

clase = Clase2_1()
next(clase.Clase2_2().firstn(5)) #line 41


```

The output of this program should be:

```python
{['Clase1_1', 'Clase1_2', 'firstn']:[37,38], ['Clase2_1', 'Clase2_2', 'firstn']:[41]
```

## How to use it

One way to use this program is to run it from the terminal. Once you have the main folder downloaded, go to `./generatorfind` and let's say you want to count the callsites in the program `/home/username/files/test.py`, then you need to do the following:

```sh
python generatorfind.py /home/username/files/test.py
```

and you will get the previously mentioned output.

You may also run your code as  package from another code you have. Simply import the following: `import generatorfind` and then do: `calls = generatorfind.main('path/to/my/program')` and then `calls` will have the dictionary with the callsites. 
