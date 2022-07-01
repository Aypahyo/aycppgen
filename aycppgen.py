import argparse

from aycppgen_core.generator import COMMAND_CREATE, ELEMENT_PROJECT, Generator, ProjectSpec, elements, commands
from aycppgen_core.wrapfilesystem import LinuxFileSystem

def create_project(name : str):
    spec = ProjectSpec(name)
    gen = Generator(LinuxFileSystem())
    gen.CreateProject(spec)

def main():
    parser = argparse.ArgumentParser("aycppgen")
    parser.add_argument("element", help=f'must be in {elements}', type=str)
    parser.add_argument("command", help=f'must be in {commands}', type=str)
    parser.add_argument("--name", dest="name", help="the name of the resource", type=str, required=True )
    args = parser.parse_args()
    if args.element in elements and args.command in commands:
        if ELEMENT_PROJECT == args.element and COMMAND_CREATE == args.command:
            create_project(args.name)
            print(f'done')
        else:
            print(f'{args.element} {args.command} not implemented')
    else:
        parser.print_help()

if __name__ == "__main__":
    main()