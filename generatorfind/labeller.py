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
    # gets rid of any unnecessary additional 'Unnamed' column
    pattern_df = pattern_df.loc[:, ~pattern_df.columns.str.contains('^Unnamed')]
    # Removes empty rows
    pattern_df = pattern_df.dropna()
    sourcemap_df = pd.read_csv(sourcemap_path, delimiter = ',')
    pattern_df = cleanNamespaceColumn(pattern_df)
    pattern_df = cleanPathColumn(pattern_df)
    generator_with_generators = getGeneratorsInSourcemap(pattern_df, sourcemap_df)
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


def getGeneratorsInSourcemap(pattern, sourcemap):
    for _index, row in pattern.iterrows():
        namespace = row['Namespace']
        pattern_line = str(row['begin_line'])
        path_for_sourcemap = row['Nombre_archivo']
        path_for_sourcemap_correct_separator = getCorrectSeparator(path_for_sourcemap)
        if namespace != 'None':
            selection = sourcemap[(sourcemap['path'] == path_for_sourcemap_correct_separator) & \
            (sourcemap['name'] == namespace) & (sourcemap['line_number'] == pattern_line)    ]
            if selection.shape[0] != 1:
                throwException(pattern, sourcemap, path_for_sourcemap, namespace, pattern_line, selection)
            yield selection

def getCorrectSeparator(path):
    path_ls = path.split('\\')
    correct_path = ''
    for item in path_ls:
        correct_path = os.path.join(correct_path, item)
    return correct_path


def throwException(pattern, sourcemap, path_for_sourcemap, namespace, pattern_line, selection):
    print(pattern.shape)
    print(f'We are looking for the row that has the parameters path: {path_for_sourcemap}; name: {namespace}; line_number: {pattern_line}')
    path_df = sourcemap[sourcemap['path'] == path_for_sourcemap]
    print(path_df.shape)
    namespace_df = sourcemap[sourcemap['name']==namespace]
    print(namespace_df.shape)
    line_df = sourcemap[sourcemap['line_number'] == pattern_line]
    print(line_df.shape)
    raise Exception(f'The data frame has {selection.shape[0]} rows')
            
            
def cleanNamespaceColumn(df):
    column = df['Namespace']
    clean_column = []
    for item in column:
        if item != 'None':
            splitted_item = item.split(',')
            last_name_unclean = splitted_item[-1]
            last_name = ''
            for letter in last_name_unclean:
                if notSpecialCharacter(letter):
                    last_name += letter
            clean_column.append(last_name)
        else:
            clean_column.append(item)
    df['Namespace'] = clean_column
    return df



def notSpecialCharacter(letter):
    if letter != ' ' and letter != '\'' and letter != ']':
        return True
    else:
        return False


def cleanPathColumn(df):
    column = df['Nombre_archivo']
    clean_column = []
    for item in column:
        if item != 'None':
            item = item.replace('\'', '').replace(' ', '')
            clean_column.append(item)
        else:
            clean_column.append(item)
    df['Nombre_archivo'] = clean_column
    return df


def getNodeIds(generator, pattern, sourcemap, ast_folder):
    filepath = ''
    for df in generator:
        node_id, new_filepath = df.iloc[0]['node_id'], df.iloc[0]['path']
        if new_filepath != filepath: #this is to prevent the file from being opened more times than necessary
            ast_df, df_path = getAstDf(new_filepath, ast_folder)
            filepath = new_filepath
        ast_df.loc[ast_df['node_id'] == node_id, 'Generator'] = 1
        ast_df = findChildren(ast_df, node_id)
        ast_df.to_csv(df_path, index = 0)
        


def getAstDf(filepath, ast_folder):
    path_with_no_file, filename = pathSeparator(filepath)
    full_path = os.path.join(ast_folder, path_with_no_file, 'label_'+filename+ '.csv')
    try:
        df = pd.read_csv(full_path, delimiter = ',')
        return (df, full_path)
    except FileNotFoundError:
        print(f'Cannot find at {full_path}')


def findChildren(df, node_id):
    ls_parents = [node_id]
    while ls_parents != []:
        # Change the value of the 'Generator' column to 1 in the corresponding nodes
        df.loc[df['parent_id'].isin(ls_parents), 'Generator'] = 1
        # Selecting the 'node_id' of the aforementioned nodes and saving it to a series
        children_df = df.loc[df['parent_id'].isin(ls_parents), 'node_id']
        #updating the value of ls_parents
        ls_parents = children_df.tolist()[:]
    return df

    
def pathSeparator(path):
    return os.path.split(path)
    
    






