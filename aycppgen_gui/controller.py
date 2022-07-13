from genericpath import exists, isdir
from logging import Logger
import os
import re
from socket import if_nameindex
from traceback import extract_tb
from setuptools import find_namespace_packages

from soupsieve import select
from aycppgen_core.FileSystemEntry import FileSystemEntry
from aycppgen_core.InterfaceManager import InterfaceManager, InterfaceSpecification
from aycppgen_core.logginghelper import logginghelper_getOrDefault
from aycppgen_core.projectmanager import ProjectManager
import PySimpleGUI as sg
from timeit import default_timer as timer
from datetime import timedelta
from aycppgen_gui.layouts import *
import PySimpleGUI as sg

class GuiController:
    def __init__(self, layout : list, 
    project_manager : ProjectManager, 
    interface_manager : InterfaceManager, 
    logger : Logger = None) -> None:
        sg.theme('DarkAmber')
        self.__logger : Logger = logginghelper_getOrDefault("GuiController", logger)
        self.__window : sg.Window = sg.Window('aycppgen', layout)
        self.__project_manager : ProjectManager = project_manager
        self.__interface_manager : InterfaceManager = interface_manager

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
        proj_name = self.__window[TAB_PROJECT_PROJECT_CREATE_NAME].get()
        self.__project_manager.create_project(proj_name)
        self.project_explorer_update_content()
        self.__window[TAB_PROJECT_PROJECT_CREATE_BUTTON].update(disabled=True)

    def PROJECT_EXPLORER_VIEW(self, values, key):
        selected_elements = values[PROJECT_EXPLORER_VIEW]
        self.__project_manager.set_project_explorer_base_selected(selected_elements)
        if len(selected_elements) == 0:
            selected = None
        else:
            selected = selected_elements[0]
        self.update_tab_interface(selected)

    def TAB_INTERFACE_TARGET_FOLDER(self, values, key):
        self.update_tab_interface_preview()
        
    def TAB_INTERFACE_NAME(self, values, key):
        self.update_tab_interface_preview()
    
    def TAB_INTERFACE_METHODS(self, values, key):
        self.update_tab_interface_preview()
    
    def TAB_INTERFACE_NAMESPACE(self, values, key):
        self.update_tab_interface_preview()

    def TAB_INTERFACE_CREATE_BUTTON(self, values, key):
        selected = self.__project_manager.get_project_explorer_base_selected()
        if selected is None or len(selected) != 1 or selected[0].IsFile():
            target_folder = None
        else:
            target_folder = selected[0].GetName()
        name = self.__window[TAB_INTERFACE_NAME].get()
        multiline_split : list = self.__window[TAB_INTERFACE_METHODS].get().split("\n")
        namespace = self.__window[TAB_INTERFACE_NAMESPACE].get()

        spec = InterfaceSpecification(
            target_folder=target_folder,
            template_interface_name=name,
            template_methods=multiline_split,
            template_namespace_name=namespace
        )
        target = self.__interface_manager.apply(spec)
        self.__interface_manager.writeInterface(target)

    def tag_project_folder_creation_target(self):
        inp : sg.Input = self.__window[TAB_PROJECT_FOLDER_CREATE_INPUT]
        folder = inp.get()
        selected_base = self.__project_manager.get_project_explorer_base()
        return f'{selected_base}/{folder}'

    def project_explorer_update_content(self):
        if self.__project_manager.try_update_project_explorer_base_content():
            lb : sg.Listbox = self.__window[PROJECT_EXPLORER_VIEW]
            lb.update(values=self.__project_manager.get_project_explorer_base_content())
            self.tab_project_folder_create_button_update_enable()
            self.tab_project_project_create_button_update_enable()

    def tab_project_folder_create_button_update_enable(self):
        creation_target = self.tag_project_folder_creation_target()
        can_create = creation_target != "" and not exists(creation_target)
        self.__window[TAB_PROJECT_FOLDER_CREATE_BUTTON].update(disabled=not can_create)

    def tab_project_project_create_button_update_enable(self):
        selected_base = self.__project_manager.get_project_explorer_base()
        self.__window[TAB_PROJECT_PROJECT_CREATE_BASE].update(selected_base)

        proj_name = self.__window[TAB_PROJECT_PROJECT_CREATE_NAME].get()
        can_create = self.__project_manager.can_create_project(proj_name)
        self.__window[TAB_PROJECT_PROJECT_CREATE_BUTTON].update(disabled=not can_create)

    def update_tab_interface(self, selected):
        if isinstance(selected, FileSystemEntry) and selected.IsDirectory():
            self.__window[TAB_INTERFACE_TARGET_FOLDER].update(selected.GetRelative())
            self.__window[TAB_INTERFACE_NAMESPACE].update("namespace")
            self.update_tab_interface_preview()
        else:
            self.__window[TAB_INTERFACE_TARGET_FOLDER].update("-- select folder ---")
            self.__window[TAB_INTERFACE_PREVIEW].update("-- select folder ---")

    def update_tab_interface_preview(self):
        selected = self.__project_manager.get_project_explorer_base_selected()
        if selected is None or len(selected) != 1 or selected[0].IsFile():
            target_folder = None
            self.__window[TAB_INTERFACE_CREATE_BUTTON].update(disabled=True)
        else:
            target_folder = selected[0].GetName()

        name = self.__window[TAB_INTERFACE_NAME].get()
        if name is None or name == "":
            name = "Iname"
            self.__window[TAB_INTERFACE_NAME].update(name)

        multiline : sg.Multiline = self.__window[TAB_INTERFACE_METHODS]
        multiline_get : str = multiline.get()
        multiline_split : list = multiline_get.split("\n")

        namespace = self.__window[TAB_INTERFACE_NAMESPACE].get()
        if namespace is None or namespace == "" or namespace == "namespace":
            namespace = self.__interface_manager.find_namespace_name(selected)
            self.__window[TAB_INTERFACE_NAMESPACE].update(namespace)

        spec = InterfaceSpecification(
            target_folder=target_folder,
            template_interface_name=name,
            template_methods=multiline_split,
            template_namespace_name=namespace
        )
        try:
            rv = self.__interface_manager.apply(spec)
            self.__window[TAB_INTERFACE_PREVIEW].update(rv.Preview())
            self.__window[TAB_INTERFACE_CREATE_BUTTON].update(disabled=False)
        except Exception as e:
            self.__window[TAB_INTERFACE_CREATE_BUTTON].update(disabled=True)
            self.__window[TAB_INTERFACE_PREVIEW].update(f'type\n{type(e)}\nmsg\n{e}')

