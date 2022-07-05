import argparse
from aycppgen_core.config import Config
from aycppgen_core.logginghelper import logginghelper_set_up_logs
from aycppgen_core.projectmanager import ProjectManager

from aycppgen_gui.controller import GuiController
from aycppgen_gui.layouts import GetLayouts

def command_selftest():
    print("looking good")

def command_gui():
    logginghelper_set_up_logs()
    config = Config()
    project_manager = ProjectManager(config)
    layouts = GetLayouts(config)
    controller = GuiController(layouts, project_manager)
    controller.run()

COMMAND_SELFTEST = "selftest"
COMMAND_GUI = "gui"

commands = [COMMAND_SELFTEST, COMMAND_GUI]

def main():
    parser = argparse.ArgumentParser("aycppgen")
    parser.add_argument("--command", help=f'must be in {commands}', required=False, type=str)
    args = parser.parse_args()
    if args.command == COMMAND_SELFTEST:
        command_selftest()
    elif args.command == COMMAND_GUI:
        command_gui()
    elif args.command == "" or args.command == None:
        command_gui()
    else:
        print(f'"{args.command}" not implemented')

if __name__ == "__main__":
    main()