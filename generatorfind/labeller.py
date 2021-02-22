from .sourcemap import Sourcemap
from .ast_to_csv import AstToCsv
import os
import csv
import pandas as pd

def main(path, name):
    #we now generate the sourcemap of the project
    sourcemapCreator(name)
    #we also generate the ast file
    astCreator(name)
    #we now obtain the names of the sourcemap
    project_name = getNameProject(name)
    sourcemap_path = 'sourcemap_' + project_name +'.csv'
    ast_path = 'LabelFolder_'+ project_name
    #we get the information we want about the labels
    pattern_df = pd.read_csv(path, delimiter = ';')
    sourcemap_df = pd.read_csv(sourcemap_path, delimiter = ',')
    pattern_df = cleanNamespaceColumn(pattern_df)
    getGeneratorIDs(pattern_df, sourcemap_df, project_name)


    

def sourcemapCreator(name):
    sourcemap = Sourcemap(name)
    sourcemap.main()
    
def astCreator(name):
    generate_ast = AstToCsv(name)
    generate_ast.main()

def getNameProject(name):
        return os.path.basename(os.path.normpath(name))


def getGeneratorIDs(pattern, sourcemap, project_name):
    for index, row in pattern.iterrows():
        if row['Namespace'] != 'None':
            


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