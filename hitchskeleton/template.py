import click
from commandlib import Command
from pathlib import Path
import os
from sys import exit
import shutil
import stat


@click.command()
@click.argument("name")
def website(name):
    homedir = Path(os.path.expanduser("~"))
    cacheroot = homedir / ".cache"
    cachedir = cacheroot / "hitchskeleton"
    currentdir = Path(os.getcwd())
    srchitch = cachedir / "hitchstory" / "examples" / "website"
    newhitchdir = currentdir / "hitch"

    if not cacheroot.exists():
        cacheroot.mkdir()

    if cachedir.exists():
        shutil.rmtree(cachedir)
    cachedir.mkdir()

    if newhitchdir.exists():
        print("Hitch already set up in this directory. Delete the folder and try again")
        exit(1)

    git = Command("git")

    git("clone", "https://github.com/hitchdev/hitchstory.git").in_dir(cachedir).run()

    shutil.copytree(srchitch / "hitch", newhitchdir)

    newrunsh = currentdir / "run.sh"
    shutil.copyfile(srchitch / "run.sh", newrunsh)
    newrunsh.chmod(newrunsh.stat().st_mode | stat.S_IEXEC)

    for existing_story in newhitchdir.joinpath("story").glob("*.story"):
        os.remove(existing_story)

    for existing_doc in newhitchdir.joinpath("docs").glob("*"):
        os.remove(existing_doc)

    click.echo("Renaming to {}".format(name))
    newhitchdir.joinpath("PROJECT_NAME").write_text(name)

    os.remove(newhitchdir / "selectors" / "selectors.yml")

    click.echo("Set up. Run ./run.sh make")
