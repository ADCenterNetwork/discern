from generatorfind.generatorfind import Discern, Discern2, FolderCalls, saveast
from fulltree.fulltree import core, FullTree
#from repos.respos import download_repos, get_repos
import sys, os, time, shutil

def main(name):
    start = time.time()
    if len(sys.argv) == 2:
        if name.endswith('.py'):
            print("***************************************\n")
            print("***Estamos trabajando con DISCERN1.***\n")
            print("***************************************\n")
            script = Discern(name)
            saveast()      
            #script.yieldfind()
            '''
            print('-----------------------------------------------------------------------------------------------------\n')
            print('In the following list we find the node\'s namespace of the generators defined in the script of interest:')
            for i in range(len(script.generators)):
                print('\n', i, ': \n', script.generators[i])
            print("----------")
            '''
            script._generatorfind()
            '''
            print('In the following list we find the namespace of the generators defined in the script of interest:')
            for i in range(len(script.generators)):
                print('\n', i, ': \n', script.generators[i])
            print("----------")
            '''
            print(script._generatorfind())
            script.assign_call_find()
        else:
            print("***************************************\n")
            print("***Estamos trabajando con FOLDER.***\n")
            print("***************************************\n")
            script = FolderCalls(name)
            script.callsites()
        
        print('LOS ASSIGNS SON LOS SIGUIENTES: ', script.assigns)
        print('LOS CALLS QUE HEMOS ENCONTRADO SON LOS SIGUIENTES: \n', script.calls)
        end = time.time()
        print("---------")
        print('Execution time:', end-start, 'seconds.')
        print('-----------------------------------------------------------------------------------------------------\n')
    elif len(sys.argv) >= 2:
        if name.endswith('.py'):
            print("***************************************\n")
            print("***Estamos trabajando con DISCERN2.***\n")
            print("***************************************\n")

            ls = sys.argv[2:]
            for i in range(len(ls)):
                ls[i] = os.path.abspath(ls[i])
            script = Discern2(name, ls)
            #saveast()      
            #script.yieldfind()
            '''
            print('-----------------------------------------------------------------------------------------------------\n')
            print('In the following list we find the node\'s namespace of the generators defined in the script of interest:')
            for i in range(len(script.generators)):
                print('\n', i, ': \n', script.generators[i])
            print("----------")
            '''
            script._generatorfind()
            '''
            print('In the following list we find the namespace of the generators defined in the script of interest:')
            for i in range(len(script.generators)):
                print('\n', i, ': \n', script.generators[i])
            print("----------")
            '''
            
            #pj = FullTree(sys.argv[-1])
            #core(pj)
            
            # TO DO 
            #get_repos(ls)
            
            script.assign_call_find()
            print('->LOS ASSIGNS SON LOS SIGUIENTES: ', script.assigns)
            print('\n-> LOS GENERATORS SON LOS SIGUIENTES: ', script.generators)
            print('\n-> LOS CALLS QUE HEMOS ENCONTRADO SON LOS SIGUIENTES: \n', script.calls)
            print('\n SOURCEMAP: ', script._mapeo())
            
            print('---------------------------------------------------------------------------------------------\n')



            #we delete the folder we created in the beginning for downloaded folders
            #shutil.rmtree('downloaded_modules', ignore_errors=True)
            
        else: 
            
            print("***************************************\n")
            print("***Estamos trabajando con FOLDER Y DISCERN2.***\n")
            print("***************************************\n")

            ls = sys.argv[2:]
            for i in range(len(ls)):
                ls[i] = os.path.abspath(ls[i])
        
            script = FolderCalls(name, ls)
            script.callsites()
            script.createids()

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
    main(sys.argv[1])
