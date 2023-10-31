import click
from commandlib import Command
from pathlib import Path
import os
from sys import exit
import shutil


@click.command()
def website():
    homedir = Path(os.path.expanduser("~"))
    cacheroot = homedir / ".cache"
    cachedir = cacheroot / "hitchskeleton"
    currentdir = Path(os.getcwd())
    srchitch = cachedir / "hitchstory" / "examples" / "website"
    newhitchdir = currentdir / "hitch"

    if not cacheroot.exists():
        cacheroot.mkdir()

    if cachedir.exists():
        cachedir.rmtree()
    cachedir.mkdir()

    if newhitchdir.exists():
        print("Hitch already set up in this directory. Delete the folder and try again")
        exit(1)

    git = Command("git")

    git("clone", "https://github.com/hitchdev/hitchstory.git").in_dir(cachedir).run()

    shutil.copytree(
        srchitch / "hitch", newhitchdir
    )

    shutil.copyfile(srchitch / "run.sh", currentdir / "run.sh")

    for existing_story in newhitchdir.joinpath("story").glob("*.story"):
        os.remove(existing_story)

    os.remove(newhitchdir / "selectors" / "selectors.yml")

    

    click.echo("Set up. Run ./run.sh make")
