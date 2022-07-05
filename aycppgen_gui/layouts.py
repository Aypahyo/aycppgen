from ctypes import alignment
from aycppgen_core.config import Config

import PySimpleGUI as sg

PROJECT_EXPLORER_VIEW = "PROJECT_EXPLORER_VIEW"
PROJECT_EXPLORER_BASE = "PROJECT_EXPLORER_BASE"

TAB_PROJECT_PROJECT_CREATE_BASE = "TAB_PROJECT_PROJECT_CREATE_BASE"
TAB_PROJECT_PROJECT_CREATE_BUTTON = "TAB_PROJECT_PROJECT_CREATE_BUTTON"
TAB_PROJECT_FOLDER_CREATE_INPUT = "TAB_PROJECT_FOLDER_CREATE_INPUT"
TAB_PROJECT_FOLDER_CREATE_BUTTON = "TAB_PROJECT_FOLDER_CREATE_BUTTON"
TAB_PROJECT_PROJECT_CREATE_NAME = "TAB_PROJECT_PROJECT_CREATE_NAME"

BUTTON_SIZE = (15, 1)


def GetLayouts(config : Config) -> list:
    project_tab = [
        [
            sg.Text( key=TAB_PROJECT_PROJECT_CREATE_BASE, expand_x=True, background_color="light grey" ),
        ],
        [
            sg.Input( key=TAB_PROJECT_FOLDER_CREATE_INPUT, expand_x=True, enable_events=True ),
            sg.Button("Create Folder", size=BUTTON_SIZE , key=TAB_PROJECT_FOLDER_CREATE_BUTTON, disabled=True)
        ],[
            sg.Input( key=TAB_PROJECT_PROJECT_CREATE_NAME, expand_x=True),
            sg.Button("Create Project", size=BUTTON_SIZE, key=TAB_PROJECT_PROJECT_CREATE_BUTTON, disabled=True)
        ]]
    layout_2 = [[sg.Text("interface")]]
    layout_3 = [[sg.Text("class")]]
    layout_4 = [[sg.Text("dto")]]
    tabgrp = sg.TabGroup(
        [[
        sg.Tab('Project', project_tab, ),
        sg.Tab('interface', layout_2),
        sg.Tab('class', layout_3), 
        sg.Tab('dto', layout_4)]],
        expand_y=True
        )
    project_explorer = [
        [sg.Text("-- select a folder --", key=PROJECT_EXPLORER_BASE), sg.FolderBrowse()],
        [
            sg.Listbox(key=PROJECT_EXPLORER_VIEW, values=[], size=(50,10)),
            tabgrp
        ]
        #[sg.Multiline( key=PROJECT_EXPLORER_VIEW )],
        #[sg.Button( button_text="foo", key="this_key" )]
        ]
    layout = project_explorer
    return layout
