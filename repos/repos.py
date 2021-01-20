import git, os
from typing import List

def _url_last_chunk(url: str) -> str:
    """Get last chunk form url, i.e. part after last '/'"""
    return url[url.rfind("/")+1:] 

def _complete_url(site: str) -> str:
    """Expand string s withouth 'http' prefix to http://github.com/{s} and strip last '/'"""
    if _url_last_chunk(site) == '': #''' This is simply to check whether or not there's a last '/' '''
        site = site[:-1] 
    if not site[:4] == 'http':
        return f'https://github.com/{site}' #This means that the site doesn't start with 'http', so we need to add it ourselves
    else:
        return site   #otherwise, 'site' is already in its complete form, so we don't need to do anything to it

def parse_urls_from_text(txt: str) -> List[str]:
    """Parse multi-line text into list of git repo urls, optionally prefixed with http://github.com/ and strip ultimate '/'"""
    fragments = txt.split('\n')
    sites = [s.strip() for s in fragments if len(s.strip()) > 0]
    return [_complete_url(s) for s in sites]


def download_repos(lst_repos : List[str], to_base_path: str) -> List[git.Repo]:
    """Clone list of git repos with depth=1 (no history); all to base path. Url of the repo name may not contain ending '/'"""
    res = []
    for repo in lst_repos:
        to_path = os.path.join(to_base_path, _url_last_chunk(repo))
        try:
            res.append(git.Repo.clone_from(repo, to_path, depth=1))
        except Exception as ex:
            print(f'GitCommandError: Repository {repo} not found')
    return res

def clone_repos(lst_repos: List[str], to_base_path: str) -> List[git.Repo]:
    """Clone list of git repos; all to base path. Url of the repo name may not contain ending '/'"""
    res = []
    for repo in lst_repos:
        to_path = os.path.join(to_base_path, _url_last_chunk(repo))
        try:
            res.append(git.Repo.clone_from(repo, to_path))
        except Exception as ex:
            print(f'GitCommandError: Repository {repo} not found')
    return res

def get_repos(full_list):
    ''' 'full_list' contains ALL of the modules that we pass as arguments to our program, regardless
    of whether they are modules in our folder of they are external. Our objective with this function
    is to determine which modules to get from github (those which are given as URLs) and download them'''
    repos_list = []
    path = os.path.join(os.getcwd(), 'downloaded_modules')
    try:
        os.mkdir(path)
    except:
        pass
    for module in full_list:
        if not os.path.exists(module): 
            #in this case, we interpret it as a github url
            repos_list.append(module)
    download_repos(repos_list, path)

