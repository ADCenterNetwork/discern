Discern README-driven Development
==================================

+ Created Feb 02, 2021 by David Minet & Alfonso Dominguez.
+ Source code: <https://github.com/ADCenterNetwork/discern>
+ Current build status: A software able to give us a source map of projects based on abstract sintax tree has been developed. It is also able to give us a first approximation about yield patterns in certain projects and where are the called during the project, relating the different files inside the project. Currently, a labeled dataset is going to be created (important question: What is the dataset going to consist of?) with the aim of introducing us to work with the deep learning model. 

---

## What is "Discern" ? 

**Discern** is a project whose idea is to have a tool developed with Deep Learning tecniques which will offer to the user the detection of software design patterns in arbitrary source code. 

The power of this software is to understand the operation as a relation of _<< metadata -> a series of processes -> data >>_ , instead of lines of code with a purpose. This is possible treating the source code as a parsed code and thanks to it we can directly obtain two important resources: a source map of the project abstract syntax tree where we can find a visual summary with general information of the nodes (with an assigned ID) and a relationship about the namespaces of the patterns we are interested in and where are them called.

Once we understand these notes, that is when deep learning work comes into play. An initial task will be to develop a labeled dataset with meaningful names in order to make easier the development. After this step, a neural network model will be developed for a later training in order to fit the model to an accurate one. 

The deep learning work will provide to us a complete abstraction about how the interest pattern is used on diferents projects and progressively the software will learn what this pattern has in common in all the projects that we offer to the neural network, obtaining conclusions that will be useful. This will be possible because deep learning will develope certain knowledges about the pattern that we aren't able, as people, to understand. 

The benefits that we will obtain after the conclusions that the model will offer us may be different. The first that come to mind may be to correct patterns in other projects or recommend other patterns to improve development.

_Note: Initially, this work has been done around "yield" patterns, but ideally we want to be able to extrapolate it to many different patterns as observers, singletons, etc._

---

## What do we need to run the project?


When Discern development is complete and a user is ready to use it, he should first understand what does Discern provide to him.

Once the user has the Discern module on his device, he should also have the project he wants to analyze. After this, he just need to decide on which pattern he wants to do the analysis.

With this elements, we can make the mental scheme: `Discern + path of the project + pattern -> file with result`.
That's to say, the user will use the Discern module on a project of interest and a pattern to analyze, and he will obtain a file will the summary of the analysis.

---

## How will Discern work?

Discern will look for any particular pattern we pass as input, in a given Python project. The file `main.py` is the one we need to run from the Terminal, and that will run the algorithm. 

So, if we have a project in a given `folder` in our directory, and we want to look for generators, we should run the following from the terminal:
```
python Discern/main.py folder generators
```
*Note: so far our project only works for generators. Once we have more functionality for other patterns in our project, we should add a list of the accepted patterns and how to run them*

---

## How the output/response will be presented to the user?


As we have mentioned, our program will look for patterns of code in whatever project you pass as input. Once this process is completed, a file called `patterns.txt` will be created in the directory you're working.

This file will contain information about all the patterns we have found. This information should be organized in the different Python files of the project, and it will mention patters can be found in that project, the lines of code where the pattern is located, and the name of the class, function, etc. of that pattern.

So, for instance, if in a certain `file.py` of our code we have the following structure:

```python
1 class Example:
2    def generator:
3        yield 'example'
```
Then in `patterns.yml` we will get the following result:
```
project/file.py:
    pattern: 
        element:           generator
        line_number:       1
        end_line_number:   3
        namespace:         ['Example', 'generator']
```
Plus, if this generator is called in `file2.py`, then we would get the following:
```
project/file2.py:
    callsite:
        line_number:       27
        end_line_number:   27
        namespace:         ['file', 'Example', 'generator']
```
In a similar way, we would get an equivalent output for patterns like singletons, decorators, composites, etc.


