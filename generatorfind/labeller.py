from .sourcemap import Sourcemap
from .ast_to_csv import AstToCsv
import os
import csv
import pandas as pd

def main(path_of_project, path_info_patterns):
    #we now generate the sourcemap of the project
    sourcemapCreator(path_of_project)
    #we also generate the ast file
    astCreator(path_of_project)
    #we now obtain the names of the sourcemap
    project_name = getNameProject(path_of_project)
    sourcemap_path = 'sourcemap_' + project_name +'.csv'
    ast_folder_path = getAstPath(project_name)
    path_info_patterns = os.path.join(os.getcwd(), path_info_patterns)
    #we get the information we want about the labels
    pattern_df = pd.read_csv(path_info_patterns, delimiter = ';')
    sourcemap_df = pd.read_csv(sourcemap_path, delimiter = ',')
    pattern_df = cleanNamespaceColumn(pattern_df)
    generator_with_generators = getGeneratorsInSourcemap(pattern_df, sourcemap_df, project_name)
    getNodeIds(generator_with_generators, pattern_df, sourcemap_df, ast_folder_path)


def sourcemapCreator(name):
    sourcemap = Sourcemap(name)
    sourcemap.main()
    
def astCreator(name):
    generate_ast = AstToCsv(name)
    generate_ast.main()

def getNameProject(name):
        return os.path.basename(os.path.normpath(name))

def getAstPath(project):
    path = os.path.join('LabelFolder_'+ project, 'LabelFolderWithGen_' + project)
    return path


def getGeneratorsInSourcemap(pattern, sourcemap, project_name):
    for _index, row in pattern.iterrows():
        namespace = row['Namespace']
        pattern_line = row['begin_line']
        path_for_sourcemap = row['Nombre_archivo']
        if namespace != 'None':
            selection = sourcemap[(sourcemap['path'] == path_for_sourcemap) & \
            (sourcemap['name'] == namespace) & (sourcemap['line_number'] == pattern_line)    ]
            if selection.shape == (0,10):
                print(f'namespace: {namespace} \npattern_line: {pattern_line} \npath_for_sourcemap: {path_for_sourcemap}')
                #TO DO raise exception when we find an empty dataframe
            yield selection
            
            
def cleanNamespaceColumn(df):
    column = df['Namespace']
    clean_column = []
    for item in column:
        if item != 'None':
            splitted_item = item.split(',')
            last_name_unclean = splitted_item[-1]
            last_name = ''
            for letter in last_name_unclean:
                if letter != ' ' and letter != '\'':
                    last_name += letter
            clean_column.append(last_name)
        else:
            clean_column.append(item)
    df['Namespace'] = clean_column
    return df


def getNodeIds(generator, pattern, sourcemap, ast_folder):
    filepath = ''
    for df in generator:
        ast_df = getAstDf(df, filepath, ast_folder)
        break
        #TO DO


def getAstDf(df, filepath, folder):
    df_path = df['path'].iloc[0]
    if df_path != filepath:
        ast_df = pd.read_csv(df_path)
        #TO DO
    






