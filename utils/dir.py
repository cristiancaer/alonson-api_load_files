from  pathlib import Path

def make_dir(path):
    if not Path(path).exists():
        Path(path).mkdir(parents=True)