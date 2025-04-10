import os
import time
import string
import PySimpleGUI as sg
import fp_scanner
import rfid_scanner
import serial
import RPi.GPIO as GPIO
import uart
# import datetime

###### Setting up the initial screen ####
if (fp_scanner.test_connection()):
    #IF connection is working
    print('Success')
else:
    exit(0)
    # if connection is not working

sg.theme('Light Brown 6')  # Set Theme
fonts = ('Any', 20)
image_file = os.path.abspath('ECE49022-SeniorDesign/Cary_Microcomputer/Cary.png')
users = []
regime = [[] for i in range(8)]
# print(fp_scanner.getEnrollCount())

with open(os.path.abspath('ECE49022-SeniorDesign/Cary_Microcomputer/users.txt')) as file:
    for line in file.readlines():
        users.append(line.strip('\n'))
    # print(users)
    
with open(os.path.abspath('ECE49022-SeniorDesign/Cary_Microcomputer/medications.txt')) as file:
    for line in file.readlines():
        times = line.split(' ')
        index = int(times[0].strip('.')) - 1
        for i in range(1, len(times)):
            regime[index].append((times[i].strip(',')).strip('\n'))

# print("please scan finger")
# lol, bool_fp = fp_scanner.matchFingerprint()
# print(lol)
# print(bool_fp)
# Initial screen layout
first_column = [[sg.Text('Hi, I\'m Cary! How can I help you today?', font=('Any', 20), justification='left', pad=((0, 0), (50, 0)))],
                [sg.Text('Current Time is: ', font=('Any', 20), justification='center')],
                [sg.Text('', key='timetext', font=('Any', 20), justification='center')],
                [sg.Text('')],
                [sg.Button('Change Schedule', font=('Any', 20), expand_x=True, expand_y=True, size=(15, 2), key="-SCH-", enable_events=True)],
                [sg.Button('Update Users', font=('Any', 20), expand_x=True, expand_y=True, key='-UPD-', enable_events=True, size=(15, 2))],
                [sg.Button('Refill', font=('Any', 20), expand_x=True, expand_y=True, size=(15, 2), key='-REFILL-')]]

flag_medDue = 0
for idx, med in enumerate(regime):
    for time_l in med:
        times = time_l.split('-')
        print(times)
        start_time = time.strptime(times[0], "%H:%M%p").tm_hour
        end_time = time.strptime(times[1], "%H:%M%p").tm_hour

        if start_time <= (time.localtime().tm_hour % 12) <= end_time:
            flag_medDue = 1
            chamber = idx
        else:
            print('not found')

# Cary image
second_column = [[sg.Image(filename=image_file)]]
layout = [[sg.Column(first_column), sg.VSeparator(), sg.Column(second_column)]]
window = sg.Window('Cary', layout, finalize=True,
                   size=(800, 480), element_justification='c', location=(0, 0))
window['timetext'].update(time.strftime('%I:%M %p'))

while True:
    # GUI Button management
    event, values = window.read(timeout=10)

    # if flag_medDue:
    #     sg.popup("A user is due for a medication! Please scan your fingerprint", font=('Any', 25), non_blocking=True, location=(0,0), line_width=25)
    #     flag_medDue = 0
    #     ret, id_fromFP = fp_scanner.matchFingerprint()
    #     if ret == True:
    #         uart.dispense(int(chamber))


    if event in (sg.WIN_CLOSED, 'Exit'):        # Window closed/program terminated
        break

    # ----- USER UPDATING SCREEN ------ #
    if event == '-UPD-':
        window.Hide()
        win2_col1 = [[sg.Text('List of current users:', size=(20, 2), font=('Any', 25), justification='center')],
                     [sg.Text('')],
                     [sg.Text('\n'.join([str(str(idx + 1) + '. ' + str(i).split('-')[0]) for idx, i in enumerate(users)]),
                              font=('Any', 15), justification='left', key='-USR-')]]
        win2_col2 = [[sg.Text('What would you like to do?',
                              font=('Any', 20), justification='center', size=(15,2))],
                     [sg.Text('')],
                     [sg.Button('Add a New User', key='-ADD-', font=('Any', 20),
                                expand_x=True, expand_y=True, size=(15, 2))],
                     [sg.Button('Remove a User', font=('Any', 20),
                                expand_x=True, expand_y=True, size=(15, 2), key='-REM-')],
                     [sg.Button('Back', font=('Any', 20), expand_x=True, expand_y=True, size=(15, 2), key='-BACK-')]]
        win2_layout = [
            [sg.Column(win2_col1, pad=((0,0), (0, 0))), sg.VerticalSeparator(), sg.Column(win2_col2, pad=((0,0), (50, 0)))]]

        win2 = sg.Window('Users', win2_layout, modal=True,
                         finalize=True, size=(800, 480), location=(0, 0))
        while True:
            ev2, vals2 = win2.read()
            # Window closed
            if ev2 == sg.WIN_CLOSED:
                win2.Close()
                window.UnHide()
                break
            # Cancel button
            if ev2 == "-BACK-":
                win2.Close()
                window.UnHide()
            # ADDING A NEW USER
            if ev2 == "-ADD-":
                win2.Hide()
                initials = list(string.ascii_uppercase)
                roles = ["Caregiver", "User"]
                win3_layout = [[sg.Text('Add a new user using the buttons below.', font=('Any', 25),
                                      expand_x=True, expand_y=False, size=(20, 2), justification='c', pad=(0, 20))],
                                      [sg.Text("First Initial"), sg.Spin(initials, expand_x=True, readonly=False, enable_events=True, text_color='black', expand_y=True, key='-IN1-', font=('Any', 20)),
                                      sg.Text("Second Initial"), sg.Spin(initials, expand_x=True, readonly=False,
                                      enable_events=True, text_color='black', expand_y=True, key='-IN2-', font=('Any', 20)),
                                      sg.Text("Third Initial"), sg.Spin(initials, expand_x=True, readonly=False,
                                      enable_events=True, text_color='black', expand_y=True, key='-IN3-', font=('Any', 20))],
                                      [sg.Text("Role"), sg.Spin(roles, expand_x=False, readonly=False, enable_events=True, text_color='black', expand_y=True, key='-ROL-', font=('Any', 20)),
                                      sg.Button("Click here to scan your fingerprint.", enable_events=True, font=('Any', 20), size=(15,2), key='-FINGER-', pad=((50,0),(0,0)))],
                                      [sg.Button('Save', font=('Any', 20), expand_x=True, expand_y=False, size=(15, 2), key='-SAVE-', pad=(0, 20)),
                                      sg.Button('Cancel', font=('Any', 20), expand_x=True, expand_y=False, size=(15, 2), pad=(0, 20), enable_events=True, key='-CANC-')]]
                win3 = sg.Window('Add New User', win3_layout, finalize=True, size=(800, 480), element_justification='c', location=(0, 0), modal=True)
                while True:
                    ev3, vals3 = win3.read()
                    # Cancel -- go back to previous screen
                    if ev3 == sg.WIN_CLOSED or ev3 == '-CANC-':
                        win3.Close()
                        win2.UnHide()
                        break
                    # Saving new user after input
                    elif ev3 == '-SAVE-':
                        person = str(
                            vals3['-IN1-'] + vals3['-IN2-'] + vals3['-IN3-'] + " - " + vals3['-ROL-'])
                        win3.Hide()
                        win2['-USR-'].update('\n'.join([str(str(idx + 1) + '. ' + str(user).split('-')[0]) for idx, user in enumerate(users)]))
                        win4_layout = [[sg.Text('Scan your fingerprint using the scanner below.', font=('Any', 20), size=(25,2), justification='center', key='FP')],
                        [sg.Image(filename='ECE49022-SeniorDesign/Cary_Microcomputer/fingerprint.png', size=(256,256),  pad=(0, 50))]]
                        # win3.Hide()
                        win4 = sg.Window('Fingerprint', win4_layout, finalize=True, size=(800, 480), element_justification='c', location=(0,0), modal=True)
                        ID = fp_scanner.newFingerprint(3, len(users))
                        if ID == b'\xff':
                            print("ERROR")
                        else:
                            print("Fingerprint saved")
                            print(ID)
                            person += " - " + ID.decode('utf-8', errors='replace')
                            with open(os.path.abspath('ECE49022-SeniorDesign/Cary_Microcomputer/users.txt'), 'a') as f:
                                f.write(person + '\n')
                                users.append(person)
                            win4.close()
                            win4_layout = [[sg.Text('Scan your RFID using the scanner below.', font=('Any', 20), size=(25,2), justification='center', key='FP')],
                                            [sg.Image(filename='ECE49022-SeniorDesign/Cary_Microcomputer/contactless.png', size=(256,256),  pad=(0, 50))]]
                            win4 = sg.Window('RFID', win4_layout, finalize=True, size=(800, 480), element_justification='c', location=(0,0), modal=True)
                            rfid_scanner.write_NFC(person)
                            win4.close()
                            win3.close()
                        fp_scanner.led_control("off","yellow")
                        # while True:
                        #     ev4, vals4 = win4.read()
                        #     # Cancel -- go back to previous screen
                        #     if ev4 == sg.WIN_CLOSED or ev4 == '-CANC-':
                        #         win4.Close()
                        #         win3.UnHide()
                        #         break
                        # win2.UnHide()
                    elif ev3 == '-FINGER-':
                        pass
                        
                            
            # USER REMOVAL
            if ev2 == '-REM-':
                win2.Hide()
                win3_col1 = [[sg.Text('List of current users:', size=(15, 2), font=('Any', 25), justification='center')],
                     [sg.Text('\n'.join([str(str(idx + 1) + '. ' + str(user).split('-')[0]) for idx, user in enumerate(users)]),
                              font=('Any', 15), justification='left', key='-USR-')]]
                win3_col2 = [[sg.Text('Select a User to Remove', font=('Any', 20), pad=((15,0), (25, 10)))],
                              [sg.Spin([str(i) for i in range(1, len(users) + 1)], expand_x=True, readonly=True,
                                                                 enable_events=True, text_color='black', expand_y=True, key='-SEL-', font=('Any', 50))],
                              [sg.Button('Delete', font=('Any', 20), expand_x=True, expand_y=False, size=(15, 2), key='-DEL-', pad=(0, 20))],
                               [sg.Button('Done', font=('Any', 20), expand_x=True, expand_y=False, size=(15, 2), key='-CANC-', pad=(0, 0))]]
                win3_layout = [[sg.Column(win3_col1, pad=((0,0), (50, 0))), sg.VerticalSeparator(), sg.Column(win3_col2, pad=((0,0), (100, 0)))]]
                win3 = sg.Window('Remove a User', win3_layout, finalize=True, size=(800, 480), element_justification='c', location=(0, 0), modal=True)
                while True:
                    ev3, vals3 = win3.read(timeout=100)
                    # Window closed (cancel button)
                    if ev3 == sg.WIN_CLOSED or ev3 == '-CANC-':
                        win3.Close()
                        win2.UnHide()
                        break
                    # Deleting selected user
                    elif ev3 == '-DEL-':
                        fpID = users[int(vals3['-SEL-']) - 1].split('-')
                        fpID = fpID[2].strip(' ')
                        fpID_bytes = fpID.encode('utf-8')
                        fp_scanner.deleteFingerprint(fpID_bytes)
                        if len(users) == 0:
                            break
                        to_pop = int(vals3['-SEL-']) - 1
                        if len(users) != 0 and to_pop < len(users): users.pop(to_pop)
                        with open(os.path.abspath('ECE49022-SeniorDesign/Cary_Microcomputer/users.txt'), 'w') as f:
                            for person in users:
                                f.write(person + '\n')
                        win3['-USR-'].update('\n'.join([str(str(idx + 1) + '. ' + user) for idx, user in enumerate(users)]))
                        win2['-USR-'].update('\n'.join([str(str(idx + 1) + '. ' + user) for idx, user in enumerate(users)])) 
                        win3['-SEL-'].update([str(i) for i in range(1, len(users))])
    # Changing medication schedule
    elif event == '-SCH-':
        window.Hide()
        win2_col1 = [[sg.Text('List of current medications:', size=(20, 2), font=('Any', 25), justification='center')],
                     [sg.Text('')],
                     [sg.Text('\n'.join([str(idx + 1) + '. ' + ', '.join(str(j) for j in i) for idx, i in enumerate(regime) if len(i) > 0]),
                              font=('Any', 15), justification='left', key='-REG-')]]
        win2_col2 = [[sg.Text('What would you like to do?', size=(15, 2),
                              font=('Any', 25), justification='center')],
                     [sg.Text('')],
                     [sg.Button('Add Medication Schedule', key='-ADD-', font=('Any', 20),
                                expand_x=True, expand_y=True, size=(15, 2))],
                     [sg.Button('Remove a Medication', font=('Any', 20),
                                expand_x=True, expand_y=True, size=(15, 2), key='-REM-')],
                     [sg.Button('Back', font=('Any', 20), expand_x=True, expand_y=True, size=(15, 2), key='-BACK-')]]
        win2_layout = [
            [sg.Column(win2_col1, pad=((0,0), (0, 0))), sg.VerticalSeparator(), sg.Column(win2_col2, pad=((0,0), (50, 0)))]]

        win2 = sg.Window('Users', win2_layout, modal=True,
                         finalize=True, size=(800, 480), location=(0, 0)) 
        while True:
            ev2, vals2 = win2.Read()
            if ev2 == sg.WIN_CLOSED or ev2 == '-BACK-':
                win2.Close()
                window.UnHide()
                break
            # New medication input submenu
            elif ev2 == '-ADD-':
                win2.Hide()
                minutes = ['00', '15', '30', '45']
                win3_layout = [[sg.Text('Add a new medication schedule using the buttons below.', font=('Any', 25),
                                      expand_x=True, expand_y=False, size=(15, 2), justification='c', pad=(0, 20))],
                             [sg.Text("Medication Number", size=(10,2)), sg.Spin([i + 1 for i in range(8)], expand_x=True, readonly=True, enable_events=True, text_color='black', expand_y=True, key='-IN1-', font=('Any', 20)),
                              sg.Text("Hour"), sg.Spin([i for i in range(1, 13, 1)], expand_x=True, readonly=True,
                                                                 enable_events=True, text_color='black', expand_y=True, key='-IN2-', font=('Any', 20)),
                              sg.Text("Minutes"), sg.Spin(minutes, expand_x=True, readonly=True,
                                                                enable_events=True, text_color='black', expand_y=True, key='-IN3-', font=('Any', 20)),
                              sg.Spin(['am', 'pm'], expand_x=True, readonly=True, enable_events=True, text_color='black', expand_y=True, key='-AMPM-', font=('Any', 20)),
                              sg.Text("to"),
                              sg.Text("Hour"), sg.Spin([i for i in range(1, 13, 1)], expand_x=True, readonly=True,
                                                                 enable_events=True, text_color='black', expand_y=True, key='-IN4-', font=('Any', 20)),
                              sg.Text("Minutes"), sg.Spin(minutes, expand_x=True, readonly=True,
                                                                enable_events=True, text_color='black', expand_y=True, key='-IN5-', font=('Any', 20)),
                              sg.Text(""), sg.Spin(['am', 'pm'], expand_x=True, readonly=True, enable_events=True, text_color='black', expand_y=True, key='-AMPM2-', font=('Any', 20))],
                             [sg.Button('Save', font=('Any', 20), expand_x=True, expand_y=False, size=(15, 2), key='-SAVE-', pad=(0, 40)),
                              sg.Button('Cancel', font=('Any', 20), expand_x=True, expand_y=False, size=(15, 2), key='-CANC-', pad=(0, 40))]]
                win3 = sg.Window('Add New Medication', win3_layout, finalize=True, size=(800, 480), element_justification='c', location=(0, 0), modal=True)
                while True:
                    ev3, vals3 = win3.Read()
                    # Window closed/cancel button
                    if ev3 == sg.WIN_CLOSED or ev3 == '-CANC-':
                        win3.Close()
                        win2.UnHide()
                        break
                    # Saving new medication after input
                    elif ev3 == '-SAVE-':
                        time_interval = str(vals3['-IN2-']) + ':' + str(vals3['-IN3-'])
                        time_interval += str(vals3['-AMPM-']) + '-'
                        time_interval += str(vals3['-IN4-']) + ':' + str(vals3['-IN5-']) + str(vals3['-AMPM2-'])

                        if time_interval not in regime[vals3['-IN1-']]:
                            regime[int(vals3['-IN1-']) - 1].append(time_interval)

                        with open(os.path.abspath('ECE49022-SeniorDesign/Cary_Microcomputer/medications.txt'), 'w') as f:
                            for idx, i in enumerate(regime):
                                if len(i) != 0:
                                    f.write(str(idx + 1) + '. ' + ', '.join([str(j) for j in i]))
                                    f.write('\n')

                        win3.Close()
                        win2['-REG-'].update('\n'.join([str(idx + 1) + '. ' + ', '.join(str(j) for j in i) for idx, i in enumerate(regime) if len(i) > 0]))
                        win2.UnHide()
            # Removal of medication
            elif ev2 == '-REM-':
                win2.Hide()
                win3_col1 = [[sg.Text('List of current medications:', size=(20, 2), font=('Any', 25), justification='center')],
                     [sg.Text('\n'.join([str(idx + 1) + '. ' + ', '.join(str(j) for j in i) for idx, i in enumerate(regime) if len(i) > 0]),
                              font=('Any', 15), justification='left', key='-REG-')]]
                win3_col2 = [[sg.Text('Select a Medication to Remove', font=('Any', 15), pad=((0,0), (25, 10)))],
                              [sg.Spin([str(idx + 1) for idx, i in enumerate(regime) if len(i) > 0], expand_x=True, readonly=True,
                                                                 enable_events=True, text_color='black', expand_y=True, key='-SEL-', font=('Any', 50))],
                              [sg.Button('Delete', font=('Any', 20), expand_x=True, expand_y=False, size=(15, 2), key='-DEL-', pad=(0, 20))],
                               [sg.Button('Done', font=('Any', 20), expand_x=True, expand_y=False, size=(15, 2), key='-CANC-', pad=(0, 0))]]
                win3_layout = [[sg.Column(win3_col1, pad=((0,0), (50, 0))), sg.VerticalSeparator(), sg.Column(win3_col2, pad=((0,0), (100, 0)))]]
                win3 = sg.Window('Remove a Medication', win3_layout, finalize=True, size=(800, 480), element_justification='c', location=(0, 0), modal=True) 
                while True:
                    ev3, vals3 = win3.read()
                    # Window closed/cancel button
                    if ev3 == '-CANC-' or sg.WIN_CLOSED:
                        win3.Close()
                        win2.UnHide()
                        break
                    # Deleting selected medication and updating files
                    elif ev3 == '-DEL-':
                        to_pop = int(vals3['-SEL-']) - 1
                        # del regime[to_pop]
                        regime[to_pop] = []
                        with open(os.path.abspath('ECE49022-SeniorDesign/Cary_Microcomputer/medications.txt'), 'w') as f:
                            for idx, i in enumerate(regime):
                                if len(i) != 0:
                                    f.write(str(idx + 1) + '. ' + ', '.join([str(j) for j in i]))
                                    f.write('\n')
                                    
                        win3['-REG-'].update('\n'.join([str(idx + 1) + '. ' + ', '.join(str(j) for j in i) for idx, i in enumerate(regime) if len(i) > 0]))
                        win2['-REG-'].update('\n'.join([str(idx + 1) + '. ' + ', '.join(str(j) for j in i) for idx, i in enumerate(regime) if len(i) > 0]))
                        win3['-SEL-'].update([str(idx + 1) for idx, i in enumerate(regime) if len(i) > 0])
    elif event == '-REFILL-':
        # sg.popup_no_buttons("Unlocking!", font=('Any', 25), auto_close_duration=5)
        # layout = [[sg.Text("Unlocking Cary!", size=(20, 2), font=('Any', 25), justification='center'),
        #            sg.Button('Done', font=('Any', 20), expand_x=True, expand_y=False, size=(15, 2), key='-CANC-', pad=(0, 0))]]
        # win2 = sg.Window('Unlock', layout, modal=True,
        #                  finalize=True, size=(800, 480), location=(0, 0))
        # window.Hide()
        uart.unlock_cary()
        popup = sg.Popup("Unlocked! Refill your medications now.", font=('Any', 25), non_blocking=False, location=(0,0), modal=True, custom_text='Done', keep_on_top=True)
        # while True:
        #     event, values = win2.read()
        #     if event == sg.WIN_CLOSED or '-CANC-':
        #         win2.Close()
        #         window.UnHide()
        #         break
        uart.lock_cary()        


    # Update the time :
    window['timetext'].update(time.strftime('%I:%M %p'))

window.close()
