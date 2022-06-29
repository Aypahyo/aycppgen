import argparse

from aycppgen_core.generator import elements, commands


def main():
    parser = argparse.ArgumentParser("simple_example")
    parser.add_argument("element", help=f'must be in {elements}', type=str)
    parser.add_argument("command", help=f'must be in {commands}', type=str)
    args = parser.parse_args()
    if args.element in elements and args.command in commands:
        print(f'{args.element} {args.command} not implemented')
    else:
        parser.print_help()

if __name__ == "__main__":
    main()