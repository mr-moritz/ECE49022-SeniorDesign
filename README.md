# **ECE49022** Senior Design, Spring 2023

<img align="right" width="200" height="200" src="https://github.com/emoritz-pu/ECE49022-SeniorDesign/blob/8cb9ca7e98d5a1d7a131ce14f424b598cb0d18f4/Cary_Microcomputer/Cary_lg.png">

## **Project Name:** Cary (*short for Apotechary*)
This repository serves to contain the code for the pill dispenser project of ECE 40922 Senior Design during Spring 2023 term.

Members:
- William Jorge
- Michael Moritz
- Yuzhou Ren
- Christopher Stephen

## Project Idea
Cary, short for Apothecary, is a personal pharmaceutical device that keeps track of your daily dosage times and amounts for up to eight different medications. It has a layer of security to keep your pharmaceuticals safe and away from the reach of children and teens, including a fingerprint scanner and an RFID tag used to authenticate each person using the device. This also make it possible for Cary to serve more than a single patient, such as a family, a group of patients at a hospital, the residents of a floor in a facilitated care facility, and more.

<img align="left" style="margin-left: 50px, margin-right: 50px" width="350" height="350" src="https://github.com/emoritz-pu/ECE49022-SeniorDesign/blob/6936a9c46c97f558c24650895a03dad59b616d7b/Cary_Microcomputer/Cary_Device.png">

## Subsystems
### GUI
The graphical user interface (GUI) is the main subsytem of the project with which the user will interact. The user will interact with the GUI for this project using a Raspberry Pi 7" touchscreen. The GUI was built using PySimpleGUI to create all button, menus, submenus, and layouts. A goal for this GUI is for it to be very simple to use, therefore for every action the user must never go past more than 3 submenus. The Python script to generate this GUI can be found at `Cary_Microcomputer/User_Interface.py`. The Raspberry Pi that is connected to our touchscreen will run the GUI application in kiosk mode, meaning that the only thing the user will see on the screen will be the GUI, front and center.

If any changes or settings need to be changed outside of the GUI application, a mouse and a keyboard can still be connected to the microcomputer to access the required functions. Additionally, a Raspberry Pi can be accessed remotely via SSH, which makes it easy to perform commands on the terminal without any sort of peripheral required.

### Fingerprint Scanner
Our system makes use of a fingerprint scanner to allow users to authenticate and receive their due medications according to the regiment that a caregiver has input. Our fignerpring scanner is equipped with an LED light ring that provides a visual queue not only when the scanner is being used, but also to communicate to the user that an action is due, such as when it is time to obtain a specific medication, for example. In our design, the fingerpring scanner is located under the Raspberry Pi 7" touchscreen to make it visible to the user and easy to access.

### RFID Tag Scanner
To interact with our system, the user not only can use the fingerprint scanner, but can also use RFID to authenticate with the device. During the proces of adding a new user, the user is required to provide their fingerprint, but also have the option to set up an RFID tag as an extra option to authenticate, and as an alternative option when it is difficult for the user to authenticate with their fingerprint.
