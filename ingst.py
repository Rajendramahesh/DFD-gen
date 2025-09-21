# Synchronous usage
from gitingest import ingest
import inspect


def codebase_tree(gitrepo_link):
    """ 
    Ingest a codebase from a given gitrepo_link (URL or local path) and return its tree structure.
    """
    summary, tree, content = ingest(gitrepo_link, exclude_patterns=[
        # Dependencies
                "node_modules/",
                "vendor/",
                "venv/",
                # Compiled files
                ".min.",
                ".pyc",
                ".pyo",
                ".pyd",
                ".so",
                ".dll",
                ".class",
                # Asset files
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".ico",
                ".svg",
                ".ttf",
                ".woff",
                ".webp",
                # Cache and temporary files
                "__pycache__/",
                ".cache/",
                ".tmp/",
                # Lock files and logs
                "yarn.lock",
                "poetry.lock",
                "*.log",
                # Configuration files
                ".vscode/",
                ".idea/",])
    return tree
#print(inspect.signature(ingest))

#res = codebase_tree("https://github.com/Rajendramahesh/DFD-gen/tree/main")

#print("after exclude Tree:", res)