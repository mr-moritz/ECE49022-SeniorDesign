import os
import time

import PySimpleGUI as sg

sg.theme('Light Brown 6')  # Set Theme
fonts = ('Any', 20)
image_file = os.path.abspath('Cary_Microcomputer/Cary.png')

first_column = [[sg.Text('Hi, I\'m Cary! How can I help you today?', font=('Any', 30), justification='left')],
                [sg.Text('Current Time is: ', font=('Any', 20), justification='center')],
                [sg.Text('', key='timetext', font=('Any', 20), justification='center')],
                [sg.Text('')],
                [sg.Button('Change Schedule', font=('Any', 10), expand_x=True, expand_y=True, key="-SCH-", enable_events=True)],
                [sg.Button('Update Users', font=('Any', 10), expand_x=True, expand_y=True, key='-UPD-', enable_events=True)],
                [sg.Button('Refill', font=('Any', 10), expand_x=True, expand_y=True)]]

second_column = [[sg.Image(filename=image_file)]]

layout = [[sg.Column(first_column), sg.VSeparator(), sg.Column(second_column)]]

window = sg.Window('Cary', layout, finalize=True)
window['timetext'].update(time.strftime('%I:%M %p'))

win2_active = False
while True:
    # GUI Button management
    new_window = sg.Window('Update Users')
    event, values = window.read(timeout=10)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == '-UPD-'  and not win2_active:
        win2_active = True
        window.Hide()
        layout2 = [[sg.Text('What would you like to do?', size=(20, 2), font=('Any', 25), justification='center')],
                   [sg.Button('Add a New User', key='-ADD-')],
                   [sg.Button('Remove a User')],
                   [sg.Button('Exit')]]

        win2 = sg.Window('Window 2', layout2, modal=True)
        while True:
            ev2, vals2 = win2.Read()
            if ev2 == sg.WIN_CLOSED or ev2 == 'Exit':
                win2.Close()
                win2_active = False
                window.UnHide()
                break
            # if ev2 == "-ADD-":
                
    # Update the time :
    window['timetext'].update(time.strftime('%I:%M %p'))
    
window.close()