from repos import parse_urls_from_text, download_repos
import click
import sys

"""Run get_repos from Command line. Uses click for command argument processing: http://zetcode.com/python/click/"""

def read_stdin():
    """Read from stdin and return string"""
    txt = ''
    for line in sys.stdin:
        txt += line
    return txt

@click.command()
@click.option('-f', '--file', type=click.File('r'), help='Read from file [FILENAME]')
@click.option('-i', '--input', is_flag=True, help='Read from standard input (stdin)')
@click.option('-b', '--base-path', default='.', type=str, help='Base path to download repos to (current dir default)')
def main(file, input, base_path):
    """get_repos ✨ - Download git repositories specified in text file or standard IN"""
    if file and input: 
        click.echo('Can''t read file and standard input at the same time')
    elif not file and not input:
          click.echo('Must provide either -f, --file of -i, --input')
    else:
        if input:
            txt = read_stdin()
        else: 
            txt = file.read()
        repos_list = parse_urls_from_text(txt)        
        download_repos(repos_list, base_path)
         

if __name__ == "__main__":
    main()
