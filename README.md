# Main

## What it does

This program has two functionalities. The first one is to read a file as input, and it will look for all the instances that every single generator function is called. The second one is the same as above, but with the singularity that first input file only searches 'calls' and the other inputs look for "generators". Those inputs could be a file or folder or both 

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

### Pass a single file as input

One way to do it, is to simply pass one file to the program. Following the example from above, if we run 
```
python main.py tests\pruebas.py
```
Then our program will look for all of the generators in that file; it will also look for all the generators that we're importing in our file from external sources, and it will return an output with the dictionary of all the namespaces of these generators as keys, and the lines in our program in which these generators were called. We can see the output of this program in the section before this one.

### Pass several files as input

In case we pass more than one program to `main.py` as input, then our program will do the following: 

It will enter all programs from the second one until the end and it will look for all the generators defined in these programs. 

Then, it will enter the first program we passed as input, and it will look if any of these generators were called in this program.

We will look at the following example: we have a folder named `folder` which contains a file called `pruebas.py`, which is exactly as appears in the introduction.

Then we have a file called `pruebas2.py` with the following code:

```python
import folder.pruebas

print(folder.pruebas.Clase1_1().Clase1_2().firstn(5))
```

So if we run 
```
python main.py tests\pruebas2.py tests\folder\pruebas.py
```

Then we get:

```python
 {('folder', 'pruebas', 'Clase1_1', 'Clase1_2', 'firstn'): [3]}
```

### Looking for generators in folders

Until now, we've only talked about the possibility of looking for generators in a single file. But let's say that you're working with a file that imports a Python module called `folder`, and you want to check if a generator is being called in your file. For example, in the file `pruebas3.py` we have:

```
import folder

folder.Clase1_1().Clase1_2().firstn(5)
```

So we want to go into `folder` to check if there are any generators, and in case there are, we want to know if any of them is being called in `pruebas3.py`, so we do:

So, for example, if we run `python main.py tests\pruebas3.py tests\folder`, and then we get:


```python
{('folder', 'Clase1_1', 'Clase1_2', 'firstn'): [3]}
```

### Looking for both calls and generators in a folder

We can pass a single folder as input, same way we did with files. In this case, it will look for all the generators in the folder, and get the instances in which these are called. 

So, if we call our program this way: `python main.py folder`, we will get this output:

```python
{'pruebas.py': {('generator',): [41, 43, 44], ('Clase1_1', 'Clase1_2', 'firstn'): [49, 56, 68, 77], ('Clase1_1', 'Clase1_3', 'firstn'): [62, 64], ('Clase2_1', 'Clase2_2', 'firstn'): [85, 89, 92, 93]}, 'prueba_simple.py': {('Clase1', 'Clase2', 'f'): [7], ('f',): [7, 19, 20, 21]}, '__init__.py': {}}
```

As you can see, we get a dictionary with all the files contained in `folder` as the keys, and the values are other dictionaries that contains the namespaces of the generators as keys, and the lines in which they were called as values.
