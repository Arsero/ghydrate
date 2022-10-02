import typer
from ghydrate import __app_name__, __version__
from rich.console import Console
import subprocess
import json
from getpass import getpass


console = Console()
app = typer.Typer()


@app.command()
def main(repo: str):
    """
    Set secret for repos
    """
    if not repo:
        typer.echo(f"{__app_name__} v{__version__}")
    else:
        secretName = input('Enter your secret name : ')
        secret = getpass('Enter your secret : ')
        repos = get_repos(repo)
        set_secret(repos, secretName, secret)
        typer.echo("\nDone\n")

    return


def get_repos(param):
    result = subprocess.run(
        ['gh', 'repo', 'list', '--json',  'nameWithOwner'], stdout=subprocess.PIPE)
    jsonRepos = json.loads(result.stdout[:-1])

    repos = []
    for name in jsonRepos:
        repos.append(name["nameWithOwner"])

    matching = [x for x in repos if param in x]
    return matching


def set_secret(repos, secret, token):
    for repo in repos:
        subprocess.run(
            ['gh', 'secret', 'set', secret, '--repo', repo], stdout=subprocess.PIPE, input=str.encode(token))
