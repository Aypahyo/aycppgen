from genericpath import exists
from logging import Logger
import os
import re
from traceback import extract_tb
from aycppgen_core.logginghelper import logginghelper_getOrDefault
from aycppgen_core.projectmanager import ProjectManager
import PySimpleGUI as sg
from timeit import default_timer as timer
from datetime import timedelta
from aycppgen_gui.layouts import *
import PySimpleGUI as sg

class GuiController:
    def __init__(self, layout : list, project_manager : ProjectManager, logger : Logger = None) -> None:
        sg.theme('DarkAmber')
        self.__logger : Logger = logginghelper_getOrDefault("GuiController", logger)
        self.__window : sg.Window = sg.Window('aycppgen', layout)
        self.__project_manager : ProjectManager = project_manager

    def run(self):
        WINDOW_READ_TIMEOUT_KEY = "WINDOW_READ_TIMEOUT_KEY"

        while True:
            event, values = self.__window.read(timeout=20, timeout_key=WINDOW_READ_TIMEOUT_KEY)
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == WINDOW_READ_TIMEOUT_KEY:
                report_handling_time = False
            else:
                report_handling_time = True
            start = timer()
            try:
                self.handle(event, values)
            except KeyError as key_error:
                self.__logger.error( "Event handler access error for: " + str(key_error))
            except Exception as e:
                self.__logger.error(f'{type(e)}: {e}')
                self.__logger.error(f'{extract_tb(e.__traceback__)}')
            end = timer()
            if report_handling_time:
                self.__logger.debug(f'{event} handling took {timedelta(seconds=end-start)} seconds')

    def handle(self, event_original : str, values):
        event_cleaned = re.sub(r"\d+$", "", event_original)
        if(event_cleaned != event_original):
            self.__logger.debug(f'{event_original} was reworked to {event_cleaned}')
        specific_handler = getattr(self, f'{event_cleaned}', None)
        if specific_handler is not None:
            specific_handler(values, event_original)
        else:
            self.__logger.warning(f'no handler named {event_cleaned} exists')

    def PROJECT_EXPLORER_BASE_BROWSER(self, values, key):
        self.__logger.info(values[key])
        print (values[key])

    def WINDOW_READ_TIMEOUT_KEY(self, values, key):
        text : sg.Text = self.__window[PROJECT_EXPLORER_BASE]
        if self.__project_manager.try_update_project_explorer_base(text.get()):
            self.__logger.info("updated to " + self.__project_manager.get_project_explorer_base())
        self.project_explorer_update_content()

    def TAB_PROJECT_FOLDER_CREATE_INPUT(self, values, key):
        self.tab_project_folder_create_button_update_enable()

    def TAB_PROJECT_FOLDER_CREATE_BUTTON(self, values, key):
        creation_target = self.tag_project_folder_creation_target()
        command = f'mkdir -p "{creation_target}"'
        os.system(command)
        self.__window[TAB_PROJECT_FOLDER_CREATE_BUTTON].update(disabled=True)

    def TAB_PROJECT_PROJECT_CREATE_BUTTON(self, values, key):
        self.__project_manager.create_project()
        self.project_explorer_update_content()
        self.__window[TAB_PROJECT_PROJECT_CREATE_BUTTON].update(disabled=True)

    def tag_project_folder_creation_target(self):
        inp : sg.Input = self.__window[TAB_PROJECT_FOLDER_CREATE_INPUT]
        folder = inp.get()
        selected_base = self.__project_manager.get_project_explorer_base()
        return f'{selected_base}/{folder}'

    def tab_project_folder_create_button_update_enable(self):
        creation_target = self.tag_project_folder_creation_target()
        can_create = creation_target != "" and not exists(creation_target)
        self.__window[TAB_PROJECT_FOLDER_CREATE_BUTTON].update(disabled=not can_create)

    def project_explorer_update_content(self):
        selected_base = self.__project_manager.get_project_explorer_base()
        if self.__project_manager.try_update_project_explorer_base_content():
            lb : sg.Listbox = self.__window[PROJECT_EXPLORER_VIEW]
            lb.update(values=self.__project_manager.get_project_explorer_base_content())
        #TODO this is misxing something - maybe these do not need to ba called all the time
        self.tab_project_folder_create_button_update_enable()
        self.__window[TAB_PROJECT_PROJECT_CREATE_BASE].update(selected_base)
        self.__window[TAB_PROJECT_PROJECT_CREATE_BUTTON].update(disabled=not self.__project_manager.can_create_project())
