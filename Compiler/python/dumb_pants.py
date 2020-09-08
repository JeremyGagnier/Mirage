import argparse
import functools
import os
import shutil
import sys

BUILD_DIRECTORY = ".dumb_pants"


# Process target
parser = argparse.ArgumentParser(description="run dumb pants")
parser.add_argument("target", metavar="target", type=str, help="target file to run")
args = parser.parse_args()

target_path = args.target
target_path_components = target_path.split('/')
target_name = target_path_components[-1]
target_base_path = '/'.join(target_path_components[:-1])
if (target_name.split('.')[-1] != 'py'):
    print(f"Specified target \"{target_path}\" is not a python file")


# Build dep tree
print("Finding dependencies")
def is_python_file(dir_entry):
    return dir_entry.is_file() and dir_entry.name.split('.')[-1] == "py"

class DependencyTree:
    def __init__(self, path, deps_found=set()):
        self.path = path

        try:
            self.code_dir_entries = list(filter(is_python_file, os.scandir(path)))
        except FileNotFoundError:
            raise Exception(f"\"{path}\" is not a directory")

        try:
            with open(f"{path}/BUILD") as dependencies_file:
                raw_dependencies = dependencies_file.read().split("\n")
                dependencies = list(filter(lambda x: x.replace(' ', '') != "", raw_dependencies))
                cyclic_dependencies = deps_found.intersection(dependencies)
                if len(cyclic_dependencies) != 0:
                    raise Exception(f"Found dependency cycle(s) at \"{path}\": {str(cyclic_dependencies)}")
                else:
                    next_deps_found = set(deps_found)
                    next_deps_found.update(path)
                    self.children = [DependencyTree(dependency, next_deps_found) for dependency in dependencies]
        except FileNotFoundError:
            raise Exception(f"BUILD file not found at \"{path}\"")
        except IOError:
            raise Exception(f"Could not open build file at \"{path}\"")

dependency_tree = DependencyTree(target_base_path)


# Copy deps into folder
# Make dir -> clean dir -> copy to dir
print("Copying dependencies")
os.makedirs(BUILD_DIRECTORY, exist_ok=True)

def remove_dir_entry(dir_entry):
    if dir_entry.is_file():
        os.remove(dir_entry.path)
    else:
        shutil.rmtree(dir_entry.path)

list(map(remove_dir_entry, os.scandir(BUILD_DIRECTORY)))

def build_dependencies(dependency_tree):
    if dependency_tree.children == []:
        return dependency_tree.code_dir_entries
    else:
        def reduce_fn(prev_deps, child_tree):
            return prev_deps + build_dependencies(child_tree)

        children_dependencies = functools.reduce(reduce_fn, dependency_tree.children, [])
        return children_dependencies + dependency_tree.code_dir_entries

dependencies = set(build_dependencies(dependency_tree))
list(map(lambda dir_entry: shutil.copy(dir_entry.path, BUILD_DIRECTORY), dependencies))


# Run target
print(f"Running \"{target_path}\"")
sys.path.append(f"{os.getcwd()}/{BUILD_DIRECTORY}") # This makes importing work
try:
    with open(f"{BUILD_DIRECTORY}/{target_name}") as target_file:
        executable = compile(target_file.read(), target_name, 'exec')
except FileNotFoundError:
    raise Exception(f"Specified target \"{target_path}\" not found")

exec(executable)
