from pathlib import Path

from lib.data.result.character.v1 import RCharacter

def walk(depth, path, value, name, root):
    print(name)
    if hasattr(root, '__annotations__'):
        # yield depth, f"class {name}:"
        for nm, clz in root.__annotations__.items():
            yield from walk(depth+1, f"{path}_{nm}", f"{value}.{nm}", nm, clz)
    else:
        yield depth, f'{path} = "{value}"'

def main():
    f = Path(__file__).parent / 'tags_category.py'
    with open(f, 'w') as f:
        for depth, line in walk(0, 'R', '', '', RCharacter):
            print(line)
            f.write(line+"\n")

if __name__ == '__main__':
    main()
