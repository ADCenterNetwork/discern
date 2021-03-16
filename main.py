from generatorfind.discern2 import Discern2
from generatorfind.folderCalls import FolderCalls
from generatorfind.ast_to_csv import AstToCsv
from generatorfind.sourcemap import Sourcemap
from generatorfind import labeller
import sys
import os
import time
import click
from new_model.software_project import SoftwareProject


'''
Discern2 is used when we only work with one file, 
and FolderCalls is for folders
'''
@click.command()
@click.argument('name', nargs = 1)
@click.option('--ast', is_flag = True, help='This generates a .csv file with the AST')
@click.option('--sourcemap', is_flag = True, help = "This generates the sourcemap of our folder")
@click.option('--calls', is_flag = True)
@click.option('--label', help = 'Enter the path of the file with the information about the generator')
def main(name, ast, sourcemap, calls, label):
    start = time.time()
    if ast:
        if isOnePythonFile(name):
            raise Exception('We can only generate ASTs of full projects')
        else:
            generate_ast = AstToCsv(name)
            generate_ast.main()
    if sourcemap:
        if isOnePythonFile(name):
            raise Exception('We can only generate ASTs of full projects')
        else:
            generate_ast = Sourcemap(name)
            generate_ast.main()
    if calls:
        if isOnePythonFile(name):
            # name is a python file name
            processPythonFile(name)
        else: 
            # name is a folder
            processFolder(name)
    if label:
        labeller.main(name, label)
 
    printExecTime(start)

def isOnePythonFile(param):
    return param.endswith('.py')

def processPythonFile(name):
    print("***************************************\n")
    print("***Estamos trabajando con DISCERN2.***\n")
    print("***************************************\n")

    ls = getFilePathsFromParam2()
    script = Discern2(name, ls)
    script._generatorfind()
    script.assign_call_find()

    print('->LOS ASSIGNS SON LOS SIGUIENTES: ', script.assigns)
    print('\n-> LOS GENERATORS SON LOS SIGUIENTES: ', script.generators)
    print('\n-> LOS CALLS QUE HEMOS ENCONTRADO SON LOS SIGUIENTES: \n', script.calls)
    print('\n SOURCEMAP: ', script._mapeo())
    print('---------------------------------------------------------------------------------------------\n')

def processFolder(name):
    print("***************************************\n")
    print("***Estamos trabajando con FOLDER Y DISCERN2.***\n")
    print("***************************************\n")
    script = FolderCalls(name)
    script.files_with_generators()
    print('Los calls son: ')
    print(script.callsites())

def getFilePathsFromParam2():
    ls = sys.argv[2:]
    for i in range(len(ls)):
        ls[i] = os.path.abspath(ls[i])
    return ls

def printExecTime(start):
    end = time.time()
    print("---------")
    tiempoej = end-start
    if tiempoej > 60:
        tiempoejmin = tiempoej // 60
        tiempoejsec = tiempoej % 60
        print('Execution time:', tiempoejmin, 'min and ', tiempoejsec,  'seconds.')
    else:
        print('Execution time:', end-start, 'seconds.')
    print('-----------------------------------------------------------------------------------------------------\n')


if __name__ == '__main__':
    SoftwareProject('c:\\projects\\discern\\new_model')
