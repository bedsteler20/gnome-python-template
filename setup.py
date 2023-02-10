import os
from re import sub


def snake_case(s):
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()


def kebab_case(s):
    return '-'.join(
        sub(r"(\s|_|-)+", " ",
            sub(r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+",
                lambda mo: ' ' + mo.group(0).lower(), s)).split())


def pascal_case(value):
    return "".join(value.title().split()).replace("_", "")


def dict_replace_str(inp: str, dat: dict[str, str]) -> str:
    for key, val in dat.items():
        inp = inp.replace(key, val)
    return inp


root = os.path.dirname(os.path.realpath(__file__))

include_dirs = [
    "build-aux",
    "src",
    "data",
    "po"
]

project_name = input("Project Name: ")
kebab_project = kebab_case(project_name)
snake_project = snake_case(kebab_project)
pascal_project = pascal_case(snake_project)

app_id = input("App Id: ")
app_id_path = app_id.replace(".", "/")

author = input("Whats your name: ")


def eval_vars(val: str):
    return dict_replace_str(val, {
        "@kebab_project@": kebab_project,
        "@snake_project@": snake_project,
        "@app_id@": app_id,
        "@app_id_path@": app_id_path,
        "@pascal_project@": pascal_project,
        "@author@": author
    })


def replace_in_file(fs: str):
    file = open(fs, "r")
    content = eval_vars(file.read())
    open(fs, "w+").write(content)


def replace_in_dir(folder: str):
    for fs in os.listdir(folder):
        fs = os.path.join(folder, fs)
        if os.path.isfile(fs):
            replace_in_file(fs)
        if os.path.isdir(fs):
            replace_in_dir(fs)
        os.rename(fs, eval_vars(fs))


for f in include_dirs:
    replace_in_dir(os.path.join(root, f))

os.rename(os.path.join(root, "src"), os.path.join(root, snake_project))
replace_in_file(os.path.join(root, "meson.build"))
