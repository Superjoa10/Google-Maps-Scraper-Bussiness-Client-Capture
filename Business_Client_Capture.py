import time
import urllib
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException, UnexpectedAlertPresentException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from tkinter import * 
from tkinter import filedialog
import pandas as pd
import os
import pyautogui as gui
from google_maps_query import main_query

from messages import txt, time_var

DRIVER_PATH = 'chromedriver.exe'

clear = lambda: os.system('cls')

head = ("""
_________                __                         _________ .__  .__               __           
\_   ___ \_____  _______/  |_ __ _________   ____   \_   ___ \|  | |__| ____   _____/  |_  ______ 
/    \  \/\__  \ \____ \   __\  |  \_  __ \_/ __ \  /    \  \/|  | |  |/ __ \ /    \   __\/  ___/ 
\     \____/ __ \|  |_> >  | |  |  /|  | \/\  ___/  \     \___|  |_|  \  ___/|   |  \  |  \___ \  
 \______  (____  /   __/|__| |____/ |__|    \___  >  \______  /____/__|\___  >___|  /__| /____  > 
        \/     \/|__|                           \/          \/             \/     \/          \/   ver. EXEMPLE 1.0
Commands:
time_loop ; start_now ; google_query ; test ; help.
        
[CTRL + C TO EXIT]""")


def open_file_dialog():
    root = Tk()
    root.withdraw()
    root.update()
    file_path = filedialog.askopenfilename()
    root.destroy()

    return file_path


def get_navegador():
    service = Service(executable_path=DRIVER_PATH)
    navegador = webdriver.Chrome(service=service)
    navegador.get("https://web.whatsapp.com/")
    while len(navegador.find_elements(By.ID, 'side')) < 1: 
        time.sleep(1)

    return navegador


def enviar_midia(navegador, midia):
    navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/div/span').click()
    attach = navegador.find_element(By.CSS_SELECTOR, ("input[type='file']"))
    attach.send_keys(midia)
    time.sleep(3)
    send = navegador.find_element(By.CSS_SELECTOR, "span[data-icon='send']")
    send.click()     


def send_message(navegador, numero, mensagem):
    max_retries = 1
    texto = urllib.parse.quote(mensagem)
    link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"

    if numero == None:
            return False, 'NONE_Number' 
    try:
        for retry in range(1, max_retries+1):
            try:
                navegador.get(link)
                WebDriverWait(navegador, timeout=50).until(EC.presence_of_element_located((By.ID, 'side')))
                time.sleep(10)
                break
            except TimeoutException:
                print(f"Timed out waiting for 'side' element to appear. Retry {retry} of {max_retries}...")
                if retry == max_retries:
                    return False, 'timeout_ERROR'
                time.sleep(10)

            except UnexpectedAlertPresentException:
                time.sleep(10)
                return False, 'Alert_text???'
            

        try:
            navegador.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button').click()
            time.sleep(5)
            return False, 'NO_WHATSAPP_Number'
        
        except NoSuchElementException:
            pass

        try:
            navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]').click()
            time.sleep(5)
            enviar_midia(navegador, "images/2916315.png") # FILE REFERENCE !!!
            time.sleep(7)
            return True, 'SUCCESS'

    
        except NoSuchElementException:
            time.sleep(5)
            return False, 'Element_ERROR'
        
        except InvalidArgumentException:
            time.sleep(5)
            return False, 'Image_ERROR'
    except:
        time.sleep(10)
        return False, 'Ambiguious_general_ERROR' 


def get_time_local():
    """ Returns a STR of the current time of day for messege generation, in portuguese """
    currentTime  = int(time.strftime('%H')) 
    if currentTime < 12 :
        return time_var[0]
    if currentTime >= 12 :
        return time_var[1]
    if currentTime > 6 :
        return time_var[2]


def main(excel_file, navegador):
    excel_file = pd.read_excel(excel_file)
    total_rows = excel_file.shape[0]

    errors = list()
    succ_int = 0
    start_ = time.perf_counter() 
    for index, row in excel_file.iterrows():
        time_now = datetime.datetime.now().strftime("%H:%M")
        buss_name = row['name']
        buss_number = row['phone_number']

        try:
                conditional_time = get_time_local()
        except:
                conditional_time = time_var[0]

        mensagem = txt(conditional_time, buss_name)
        buss_number = str('55' + str(buss_number))

        send = send_message(navegador, buss_number, mensagem)
        print(f"""
Runned at {time_now}, Nº: {index}/{total_rows - 1}
Name: {buss_name}
LOG: {send}
-----------------------------------------------""")
        
        if send[0] == False:
            errors.append({'Name': buss_name, 'Error':send[1]})
        elif send[0] == True:
            succ_int += 1

    clear()
    finish_ = time.perf_counter()
    final_time = round(int(finish_- start_) / 60)
    print(f'''
Done Running! {time_now}, runned in {final_time} minutes
Successfull messages = {succ_int}/{total_rows - 1}
Errors = {len(errors)}/{total_rows - 1}''')
    while True:
        response_final = input("""--------------------------
Would you like to see more details about the run?
Erros ; Exit.""")
        if response_final.casefold() == 'Erros'.casefold():
            for error in errors:
                print(error)         

        if response_final.casefold() ==  "back".casefold():
            print('exiting...')
            break          
        
        else:
            print("Please Write a valid command!")


def test_message():
    number = input('''
Please insert a number in which to test. INSTRUCTIONS: Can be your own number, must contain region code exemple (11 95555-5555)
N:''')
    number = str(str(55) + number)
    start_ = time.perf_counter() 

    try:
        conditional_time = get_time_local()
    except:
        conditional_time = time_var[0]

    mensagem = txt(conditional_time)

    print("opening web driver ...")
    navegador = get_navegador()

    send = send_message(navegador, number, mensagem)
    finish_ = time.perf_counter()
    final_time = round(int(finish_- start_) / 60)
    if send[0] == False:
        print(f'''
Fail! - reason: {send[1]}
took {final_time} minutes
--------------------------''')
        
    else:
        print(f'''
Success! 
took {final_time} minutes
--------------------------''')


def test_file():
    print("getting file location ...")
    file_name = open_file_dialog()
    excel_file = pd.read_excel(file_name)
    total_rows = excel_file.shape[0]
    for index, row in excel_file.iterrows():
        time = datetime.datetime.now().strftime("%H:%M")
        buss_name = row['name']
        buss_address = row['address']
        buss_number = row['phone_number']
        buss_web_site = row['website']

        print(f"""
Runned at {time}, Nº: {index}/{total_rows - 1}
Name: {buss_name}
Address: {buss_address}]
Number: {buss_number}
Website: {buss_web_site}
------------------------------------------------""")


def help():
    print("""
Project Info:
    A python automation, command line tool that, contains 2 tools within. One being a google maps query tool, that given a business and a location, queries about 120 business information, like phone number which can be user to later automatically send messages and files to them using the second tool.

Commands:
    Time_loop - Given a hour of the day, it'll store the Whatsapp login using the QrCode, 
    then starts a clock,  that if the PC is not turned of, will start to message the given file's numbers.
          
    start_now - Asks for the whatsapp login, then for a csv or excel file, after it imidietly starts sending messages.
          
    google_query - Given a location, and a business type, it query the number and information of all found business on the location. for more information on how it does this, look at the github repository
    
    Test - test main functionalaties of the app, such as file compatibility, chrome conection and how the message and file look when sent on whatsapp

A project by Superjoa10!
https://github.com/Superjoa10 
          
Go BACK? ...
""")
    while True:
        response = input("")
        if response.casefold() == "back".casefold():
            break
        else:
             print('to exit write "back" as a command')



if __name__ == "__main__":# Command prompt and time loop
    print(head)
    while True:
        response_command = input()

        if response_command.casefold() ==  "time_loop".casefold():
            print("getting file location ...")
            print('select a Excel file generates by google_maps_query.py or formated like "name, address, website, number"')
            excel_file = open_file_dialog()

            print("opening web driver ...")
            navegador = get_navegador()

            x = datetime.datetime.now().strftime("%H:%M")
            y = input('When do you want to run?  USAGE: 08 or 12 ; must be just the number, it its 8 must have 0 before ')
            y = str(y + ':00')
            while x != y:
                print(f"Now {x}!  Waiting to reach time {y}, updating in 60 seconds...   [CTRL + C TO BREAK OUT OF LOOP]")
                time.sleep(60)
                gui.press('shift')
                x = datetime.datetime.now().strftime("%H:%M")
                
            else:
                print(f'Time reached {y}!!!')
                main(excel_file, navegador)
                print(head)

        elif response_command.casefold() == 'start_now'.casefold():
                print("getting file location ...")
                excel_file = open_file_dialog()

                print("opening web driver ...")
                navegador = get_navegador()

                main(excel_file, navegador)
                print(head)

        elif response_command.casefold() == 'google_query'.casefold():
                neach = input('Name to query: ')
                location = input('Location to query: ')
                search_for =  str(neach + ' ' +  location)
                total = int(input('Number of places to query: '))

                main_query(search_for, total, location)
                print('file saved at seleceted directory')
                print(head)

        elif response_command.casefold() == 'test'.casefold():
                clear()
                print('''
What would you like to test?    
Options:
test_file_comp ; test_message ; back.''')
                while True:
                    response_test = input()
                    if response_test.casefold() == 'test_message'.casefold():
                        clear()
                        test_message()
                        break

                    elif response_test.casefold() == 'test_file_comp'.casefold():
                        clear()
                        test_file()
                        break

                    elif response_test.casefold() == 'back'.casefold():
                        clear()
                        print('Going back... ')
                        break

                    else:
                        print("Please Write a valid command!")

                print(head)

        elif response_command.casefold() == 'help'.casefold():
                clear()
                help()
                clear()
                print(head)

        else:
                print("Please Write a valid command!")
    