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

TAB_INTERFACE_TARGET_FOLDER = "TAB_INTERFACE_TARGET_FOLDER"
TAB_INTERFACE_NAMESPACE = "TAB_INTERFACE_NAMESPACE"
TAB_INTERFACE_NAME = "TAB_INTERFACE_NAME"
TAB_INTERFACE_METHODS = "TAB_INTERFACE_METHODS"
TAB_INTERFACE_PREVIEW = "TAB_INTERFACE_PREVIEW"
TAB_INTERFACE_CREATE_BUTTON = "TAB_INTERFACE_CREATE_BUTTON"

BUTTON_SIZE = (15, 1)


def GetLayouts(config : Config) -> list:
    project_tab = [[
            sg.Text( key=TAB_PROJECT_PROJECT_CREATE_BASE, expand_x=True, background_color="light grey" )
        ],[
            sg.Input( key=TAB_PROJECT_FOLDER_CREATE_INPUT, expand_x=True, enable_events=True ),
            sg.Button("Create Folder", size=BUTTON_SIZE , key=TAB_PROJECT_FOLDER_CREATE_BUTTON, disabled=True)
        ],[
            sg.Input( key=TAB_PROJECT_PROJECT_CREATE_NAME, expand_x=True),
            sg.Button("Create Project", size=BUTTON_SIZE, key=TAB_PROJECT_PROJECT_CREATE_BUTTON, disabled=True)
        ]]
    layout_2 = [[
            sg.Text("-- select folder ---", key=TAB_INTERFACE_TARGET_FOLDER, expand_x=True, background_color="light grey" )
        ],[
            sg.Input("namespace", key=TAB_INTERFACE_NAMESPACE, expand_x=True, enable_events=True)
        ],[
            sg.Input("Iname", key=TAB_INTERFACE_NAME, expand_x=True, enable_events=True)
        ],[
            sg.Multiline("int foo()", size=(1,5), key=TAB_INTERFACE_METHODS, expand_x=True, enable_events=True)
        ],[
            sg.HorizontalSeparator()
        ],[
            sg.Multiline("--- preview ---", size=(80,20), expand_x=True, key=TAB_INTERFACE_PREVIEW)
        ],[
            sg.Button("Create Interface", size=BUTTON_SIZE, key=TAB_INTERFACE_CREATE_BUTTON, disabled=True)
        ]]

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
            sg.Listbox(key=PROJECT_EXPLORER_VIEW, values=[], size=(80,10), enable_events=True),
            tabgrp
        ]
        #[sg.Multiline( key=PROJECT_EXPLORER_VIEW )],
        #[sg.Button( button_text="foo", key="this_key" )]
        ]
    layout = project_explorer
    return layout
