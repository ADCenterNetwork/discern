from generatorfind.generatorfind import Discern2, FolderCalls, saveast
#from repos.respos import download_repos, get_repos
import sys, os, time, shutil

'''
Discer2 is used when we only work with one file, 
and FolderCalls is for folders
'''

def main(name):
    start = time.time()
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

        '''
        ls = sys.argv[2:]
        for i in range(len(ls)):
            ls[i] = os.path.abspath(ls[i])
            '''
    
        script = FolderCalls(name)
        script.files_with_generators()
        print('Los calls son: ')
        print(script.callsites())
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
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        raise IndexError('Expected at least two arguments')
