import PySimpleGUI as sg
import Models.init as main
import Models.fees as feesModel

feesHeadings = ["FEE", "GRADE"]

def fess_window(yearN):
    layout = [
        [sg.T("Fee:"), sg.I(key="fee", size=(20, 1)), sg.T("Grade:"),
         sg.OptionMenu(values=main.getConstants("grades"), key="grade", size=(20, 1))],
        [sg.Button("ADD", key="add_btn"), sg.Button("DELETE", key="delete_btn"), sg.Button("EDIT", key="edit_btn"), sg.Button("CLEAR", key="clear_btn")],
        [sg.Table(values=feesModel.Fees(yearN).getAll(), headings=feesHeadings, key="-TABLE-",
                  auto_size_columns=True, expand_x=True, expand_y=True, justification='c', enable_events=True, display_row_numbers=True)]
    ]

    window = sg.Window("Fees List", layout, margins=(10, 10), element_justification='c',
                       resizable=True, finalize=True, size=(600, 400))
    window['-TABLE-'].expand(True, True)

    def clearValues():
        window['fee'].update(value='')
        window['grade'].update(value='')
        window["-TABLE-"].update(feesModel.Fees(yearN).getAll())

    while True:
        event, values = window.read()
        if event in ("Exit", sg.WIN_CLOSED):
            break
        elif event == "clear_btn":
            clearValues()
        elif event == "add_btn":
            try:
                feeOBJ = [str(values['fee']).replace(',',''), values['grade']]
                feesModel.Fees(yearN).add(feeOBJ)
                clearValues()
            except:
                sg.popup("Invalid information")
        elif event == "edit_btn":
            try:
                currentEntries = window["-TABLE-"].get()
                i = values["-TABLE-"][0]
                grade = values['grade']
                fee = values['fee']
                if values['fee'] == '': fee = currentEntries[i][0]
                if values['grade'] == '': grade = currentEntries[i][1]
                feeOBJ = [str(fee).replace(',',''), grade]
                feesModel.Fees(yearN).edit(currentEntries[i][-1], feeOBJ)
                clearValues()
            except:
                sg.popup("Invalid information")
        elif event == "delete_btn":
            feesModel.Fees(yearN).delete(currentEntries[i][-1])
            clearValues()
    window.close()
