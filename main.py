from generatorfind.discern2 import Discern2
from generatorfind.folderCalls import FolderCalls
import sys, os, time

'''
Discer2 is used when we only work with one file, 
and FolderCalls is for folders
'''
def main(name):
    start = time.time()
    if isOnePythonFile(name):
        # name is a python file name
        processPythonFile(name)
    else: 
        # name is a folder
        processFolder(name)

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
    script.createids()

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
        tiempoejmin = tiempoej//60
        tiempoejsec = tiempoej%60
        print('Execution time:', tiempoejmin, 'min and ', tiempoejsec,  'seconds.')
    else:
        print('Execution time:', end-start, 'seconds.')
    print('-----------------------------------------------------------------------------------------------------\n')

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        raise IndexError('Expected at least two arguments')
    




