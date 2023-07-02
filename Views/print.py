import PySimpleGUI as sg
import Models.init as main
import Models.print as printModel

def print_reports_menu(yearN):
    layout = [
        [sg.T("Grade:"), sg.OptionMenu(values=main.getConstants("grades"), default_value='', key="gradeNum"),
         sg.T("Class:"), sg.OptionMenu(values=main.getConstants("classes"), default_value='', key="classNum")],
        [sg.T("Month:"), sg.I(key="monthNum", size=(5, 1)),
         sg.T("Year:"), sg.I(key="yearNum", size=(5, 1))],
        [sg.T("Folder:"), sg.I(key="folderPath", disabled=True)],
        [sg.Button("SELECT FOLDER", key="folder_btn", expand_x=True)],
        [sg.Button("COPY REPORTS TO FOLDER", key="copy_btn"),
         sg.Button("Canel", key="Exit")]
    ]

    window = sg.Window("Print Reports", layout, margins=(10, 10),
                       element_justification='c', resizable=True, finalize=True,
                       size=(400, 250))
    while True:
        event, values = window.read()
        if event in ("Exit", sg.WIN_CLOSED):
            break
        elif event == "folder_btn":
            folder = sg.popup_get_folder("Folder to copy reports to:", "Folder Selector")
            window['folderPath'].update(value=folder)
            continue
        elif event == "copy_btn":
            try:
                if values['gradeNum'] == '' or values['classNum'] == '' or values['monthNum'] == '' or values['yearNum'] == '' or values['folderPath'] == '':
                    sg.popup("There was missing information...", title="Did you miss something?")
                    continue
                printModel.Print(yearN).printAll(values['gradeNum'], values['classNum'],
                                            values['monthNum'],values['yearNum'],
                                            values['folderPath'])
                sg.popup("Copied reports successfully!", title="Done")
                break
            except:
                sg.popup("Invalid information")
    window.close()
