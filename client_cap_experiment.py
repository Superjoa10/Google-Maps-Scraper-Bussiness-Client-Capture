import time
import urllib
import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException, UnexpectedAlertPresentException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tkinter import * 
from tkinter import filedialog
import pandas as pd
import os
from google_maps_query import main_query
from configparser import ConfigParser
import pyautogui as gui

clear = lambda: os.system('cls')

head = ("""
_________                __                         _________ .__  .__               __           
\_   ___ \_____  _______/  |_ __ _________   ____   \_   ___ \|  | |__| ____   _____/  |_  ______ 
/    \  \/\__  \ \____ \   __\  |  \_  __ \_/ __ \  /    \  \/|  | |  |/ __ \ /    \   __\/  ___/ 
\     \____/ __ \|  |_> >  | |  |  /|  | \/\  ___/  \     \___|  |_|  \  ___/|   |  \  |  \___ \  
 \______  (____  /   __/|__| |____/ |__|    \___  >  \______  /____/__|\___  >___|  /__| /____  > 
        \/     \/|__|                           \/          \/             \/     \/          \/   ver. experimental 1.0
Commands:
time_loop ; start_now ; google_query ; test ; options ; help.
        
[CTRL + C TO EXIT]""")


pt_txt = lambda Horario, Nome:  (f"""{Horario}, representante da {Nome}, Como vai?  
Esse é meu projetp""")

eng_txt = lambda Horario, Nome: (f"""{Horario}, Representative da {Nome}. My nome é Superjoa10, ant this is my project""")


def get_settings():#TODO
    '''
    parser = ConfigParser()
    parser.read("configs.ini")
    message = parser.get('settings', 'message')
    '''

    global CONTRY_AVARAGE, TIME_AVARAGE, MESSAGE_LANGUAGE
    CONTRY_AVARAGE = 'brazil'
    TIME_AVARAGE = 'Bom dia', 'Good morning'
    MESSAGE_LANGUAGE = 'portugues'


def open_file_dialog():
    print('select a CSV file generates by google_maps_query.py or formated like "name, address, website, number"')
    root = Tk()
    root.withdraw()
    root.update()
    file_path = filedialog.askopenfilename()
    root.destroy()

    return file_path


def get_navegador():
    navegador = webdriver.Chrome()
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
    max_retries = 1 # TODO make this a get_settings paremeter
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
            enviar_midia(navegador, "images/2916315.png")
            time.sleep(3)
            enviar_midia(navegador, "images/2916315.png")
            
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


def get_greeting_and_time(country_name):
    country_timezones = {
    'Afghanistan': 'Asia/Kabul',
    'Albania': 'Europe/Tirane',
    'Algeria': 'Africa/Algiers',
    'Andorra': 'Europe/Andorra',
    'Angola': 'Africa/Luanda',
    'Antigua and Barbuda': 'America/Antigua',
    'Argentina': 'America/Argentina/Buenos_Aires',
    'Armenia': 'Asia/Yerevan',
    'Australia': 'Australia/Sydney',
    'Austria': 'Europe/Vienna',
    'Azerbaijan': 'Asia/Baku',
    'Bahamas': 'America/Nassau',
    'Bahrain': 'Asia/Bahrain',
    'Bangladesh': 'Asia/Dhaka',
    'Barbados': 'America/Barbados',
    'Belarus': 'Europe/Minsk',
    'Belgium': 'Europe/Brussels',
    'Belize': 'America/Belize',
    'Benin': 'Africa/Porto-Novo',
    'Bhutan': 'Asia/Thimphu',
    'Bolivia': 'America/La_Paz',
    'Bosnia and Herzegovina': 'Europe/Sarajevo',
    'Botswana': 'Africa/Gaborone',
    'Brazil': 'America/Sao_Paulo',
    'Brasil': 'America/Sao_Paulo',
    'Brunei': 'Asia/Brunei',
    'Bulgaria': 'Europe/Sofia',
    'Burkina Faso': 'Africa/Ouagadougou',
    'Burundi': 'Africa/Bujumbura',
    'Cambodia': 'Asia/Phnom_Penh',
    'Cameroon': 'Africa/Douala',
    'Canada': 'America/Toronto',
    'Cape Verde': 'Atlantic/Cape_Verde',
    'Central African Republic': 'Africa/Bangui',
    'Chad': 'Africa/Ndjamena',
    'Chile': 'America/Santiago',
    'China': 'Asia/Shanghai',
    'Colombia': 'America/Bogota',
    'Comoros': 'Indian/Comoro',
    'Congo (Brazzaville)': 'Africa/Brazzaville',
    'Congo (Kinshasa)': 'Africa/Kinshasa',
    'Costa Rica': 'America/Costa_Rica',
    'Croatia': 'Europe/Zagreb',
    'Cuba': 'America/Havana',
    'Cyprus': 'Asia/Nicosia',
    'Czech Republic': 'Europe/Prague',
    'Denmark': 'Europe/Copenhagen',
    'Djibouti': 'Africa/Djibouti',
    'Dominica': 'America/Dominica',
    'Dominican Republic': 'America/Santo_Domingo',
    'East Timor': 'Asia/Dili',
    'Ecuador': 'America/Guayaquil',
    'Egypt': 'Africa/Cairo',
    'El Salvador': 'America/El_Salvador',
    'Equatorial Guinea': 'Africa/Malabo',
    'Eritrea': 'Africa/Asmara',
    'Estonia': 'Europe/Tallinn',
    'Eswatini': 'Africa/Mbabane',
    'Ethiopia': 'Africa/Addis_Ababa',
    'Fiji': 'Pacific/Fiji',
    'Finland': 'Europe/Helsinki',
    'France': 'Europe/Paris',
    'Gabon': 'Africa/Libreville',
    'Gambia': 'Africa/Banjul',
    'Georgia': 'Asia/Tbilisi',
    'Germany': 'Europe/Berlin',
    'Ghana': 'Africa/Accra',
    'Greece': 'Europe/Athens',
    'Grenada': 'America/Grenada',
    'Guatemala': 'America/Guatemala',
    'Guinea': 'Africa/Conakry',
    'Guinea-Bissau': 'Africa/Bissau',
    'Guyana': 'America/Guyana',
    'Haiti': 'America/Port-au-Prince',
    'Honduras': 'America/Tegucigalpa',
    'Hungary': 'Europe/Budapest',
    'Iceland': 'Atlantic/Reykjavik',
    'India': 'Asia/Kolkata',
    'Indonesia': 'Asia/Jakarta',
    'Iran': 'Asia/Tehran',
    'Iraq': 'Asia/Baghdad',
    'Ireland': 'Europe/Dublin',
    'Israel': 'Asia/Jerusalem',
    'Italy': 'Europe/Rome',
    'Jamaica': 'America/Jamaica',
    'Japan': 'Asia/Tokyo',
    'Jordan': 'Asia/Amman',
    'Kazakhstan': 'Asia/Almaty',
    'Kenya': 'Africa/Nairobi',
    'Kiribati': 'Pacific/Tarawa',
    'Korea, North': 'Asia/Pyongyang',
    'Korea, South': 'Asia/Seoul',
    'Kuwait': 'Asia/Kuwait',
    'Kyrgyzstan': 'Asia/Bishkek',
    'Laos': 'Asia/Vientiane',
    'Latvia': 'Europe/Riga',
    'Lebanon': 'Asia/Beirut',
    'Lesotho': 'Africa/Maseru',
    'Liberia': 'Africa/Monrovia',
    'Libya': 'Africa/Tripoli',
    'Liechtenstein': 'Europe/Vaduz',
    'Lithuania': 'Europe/Vilnius',
    'Luxembourg': 'Europe/Luxembourg',
    'Madagascar': 'Indian/Antananarivo',
    'Malawi': 'Africa/Blantyre',
    'Malaysia': 'Asia/Kuala_Lumpur',
    'Maldives': 'Indian/Maldives',
    'Mali': 'Africa/Bamako',
    'Malta': 'Europe/Malta',
    'Marshall Islands': 'Pacific/Majuro',
    'Mauritania': 'Africa/Nouakchott',
    'Mauritius': 'Indian/Mauritius',
    'Mexico': 'America/Mexico_City',
    'Micronesia': 'Pacific/Pohnpei',
    'Moldova': 'Europe/Chisinau',
    'Monaco': 'Europe/Monaco',
    'Mongolia': 'Asia/Ulaanbaatar',
    'Montenegro': 'Europe/Podgorica',
    'Morocco': 'Africa/Casablanca',
    'Mozambique': 'Africa/Maputo',
    'Myanmar': 'Asia/Yangon',
    'Namibia': 'Africa/Windhoek',
    'Nauru': 'Pacific/Nauru',
    'Nepal': 'Asia/Kathmandu',
    'Netherlands': 'Europe/Amsterdam',
    'New Zealand': 'Pacific/Auckland',
    'Nicaragua': 'America/Managua',
    'Niger': 'Africa/Niamey',
    'Nigeria': 'Africa/Lagos',
    'North Macedonia': 'Europe/Skopje',
    'Norway': 'Europe/Oslo',
    'Oman': 'Asia/Muscat',
    'Pakistan': 'Asia/Karachi',
    'Palau': 'Pacific/Palau',
    'Panama': 'America/Panama',
    'Papua New Guinea': 'Pacific/Port_Moresby',
    'Paraguay': 'America/Asuncion',
    'Peru': 'America/Lima',
    'Philippines': 'Asia/Manila',
    'Poland': 'Europe/Warsaw',
    'Portugal': 'Europe/Lisbon',
    'Qatar': 'Asia/Qatar',
    'Romania': 'Europe/Bucharest',
    'Russia': 'Europe/Moscow',
    'Rwanda': 'Africa/Kigali',
    'Saint Kitts and Nevis': 'America/St_Kitts',
    'Saint Lucia': 'America/St_Lucia',
    'Saint Vincent and the Grenadines': 'America/St_Vincent',
    'Samoa': 'Pacific/Apia',
    'San Marino': 'Europe/San_Marino',
    'Sao Tome and Principe': 'Africa/Sao_Tome',
    'Saudi Arabia': 'Asia/Riyadh',
    'Senegal': 'Africa/Dakar',
    'Serbia': 'Europe/Belgrade',
    'Seychelles': 'Indian/Mahe',
    'Sierra Leone': 'Africa/Freetown',
    'Singapore': 'Asia/Singapore',
    'Slovakia': 'Europe/Bratislava',
    'Slovenia': 'Europe/Ljubljana',
    'Solomon Islands': 'Pacific/Guadalcanal',
    'Somalia': 'Africa/Mogadishu',
    'South Africa': 'Africa/Johannesburg',
    'South Sudan': 'Africa/Juba',
    'Spain': 'Europe/Madrid',
    'Sri Lanka': 'Asia/Colombo',
    'Sudan': 'Africa/Khartoum',
    'Suriname': 'America/Paramaribo',
    'Sweden': 'Europe/Stockholm',
    'Switzerland': 'Europe/Zurich',
    'Syria': 'Asia/Damascus',
    'Taiwan': 'Asia/Taipei',
    'Tajikistan': 'Asia/Dushanbe',
    'Tanzania': 'Africa/Dar_es_Salaam',
    'Thailand': 'Asia/Bangkok',
    'Togo': 'Africa/Lome',
    'Tonga': 'Pacific/Tongatapu',
    'Trinidad and Tobago': 'America/Port_of_Spain',
    'Tunisia': 'Africa/Tunis',
    'Turkey': 'Europe/Istanbul',
    'Turkmenistan': 'Asia/Ashgabat',
    'Tuvalu': 'Pacific/Funafuti',
    'Uganda': 'Africa/Kampala',
    'Ukraine': 'Europe/Kiev',
    'United Arab Emirates': 'Asia/Dubai',
    'United Kingdom': 'Europe/London',
    'United States': 'America/New_York',
    'Uruguay': 'America/Montevideo',
    'Uzbekistan': 'Asia/Tashkent',
    'Vanuatu': 'Pacific/Efate',
    'Vatican City': 'Europe/Vatican',
    'Venezuela': 'America/Caracas',
    'Vietnam': 'Asia/Ho_Chi_Minh',
    'Yemen': 'Asia/Aden',
    'Zambia': 'Africa/Lusaka',
    'Zimbabwe': 'Africa/Harare'
}

    if country_name.casefold() in country_timezones:
        country_name = country_name.lower()
        timezone = pytz.timezone(country_timezones[country_name])
        current_time = datetime.datetime.now(timezone)
        hour = current_time.hour

        if 5 <= hour < 12:
            return 'Good morning!'
        elif 12 <= hour < 18:
            return 'Good afternoon!'
        else:
            return 'Good evening!'
    else:
        print(f'the country {country_name} is invalid, using defined avarage country time')
        return None


def get_time_local():
    """ Returns a STR of the current time of day for messege generation, in portuguese """
    currentTime  = int(time.strftime('%H')) 
    if currentTime < 12 :
        return('Bom dia')
    if currentTime >= 12 :
        return('Boa tarde')
    if currentTime > 6 :
        return('Boa noite')


def extract_state_and_country(address):
    address_parts = address.split(',')
    country = address_parts[-1].strip()

    return country


def main(excel_file, navegador):
    excel_file = pd.read_excel(excel_file)
    total_rows = excel_file.shape[0]

    errors = list()
    succ_int = 0
    start_ = time.perf_counter() 
    for index, row in excel_file.iterrows():
        time_now = datetime.datetime.now().strftime("%H:%M")
        buss_name = row['name']
        buss_address = row['address']
        buss_number = row['phone_number']
        #buss_web_site = row['website'] # TODO

        if MESSAGE_LANGUAGE == 'portugues':
            try:
                conditional_time = get_time_local()
            except:
                conditional_time = TIME_AVARAGE[0]
            mensagem = pt_txt(conditional_time, buss_name)
            buss_number = str('55' + str(buss_number))

        if MESSAGE_LANGUAGE == 'ingles':
            country = extract_state_and_country(buss_address)
            if not country:
                country = CONTRY_AVARAGE
                        
            conditional_time = get_greeting_and_time(country)
            if conditional_time == None:
                conditional_time = TIME_AVARAGE[1]
            mensagem = eng_txt(conditional_time, buss_name)

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
            print('exiting ')
            break          
        
        else:
            print("Please Write a valid command!")


def test_message():
    number = input('''
Please insert a number in which to test. INSTRUCTIONS: Can be your own number, must contain region code exemple (11 95555-5555)
N:''')
    
    start_ = time.perf_counter() 
    buss_name, buss_address = 'TEST BUSSINESS NAME', 'PLACEHOLDER'

    if MESSAGE_LANGUAGE == 'portugues':
            try:
                conditional_time = get_time_local()
            except:
                conditional_time = TIME_AVARAGE[0]

            mensagem = pt_txt(conditional_time, buss_name)

    if MESSAGE_LANGUAGE == 'ingles':
            country = extract_state_and_country(buss_address)
            if not country:
                country = CONTRY_AVARAGE
                        
            conditional_time = get_greeting_and_time(country)
            if conditional_time == None:
                conditional_time = TIME_AVARAGE[1]

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


def test_file(): #TODO MAKE RETURN SUCESS OR FAIL
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
    

def options(): #TODO
    print("""
          Select options
-------------------------------------
            Language 
           ENG ; PT-BR
          
            Message
*select to see current one and change it*
          
             Image
*select to see current ones file location, 
can be None or multiple*
          
        Default_Country_time
*by default the program extracts the country from the address of the bussness
and gets the time, so it can generate the message properly, if unsuccsessfull it'll use the one
defined here*
current: {current_defalt_country}

          
OR back""")
    
    while True:
        response_options = input()
        if response_options.casefold() ==  "language".casefold():
            pass

        if response_options.casefold() ==  "message".casefold():
            pass

        if response_options.casefold() ==  "image".casefold():
            pass
        
        if response_options.casefold() ==  "Default_Country_time".casefold():
            print('''---------------------
Parameters: 
None - Will ask when running every time it can't extract from bussness adress, breaks the automatic nature of the program;
                  
Country Name - will ask for the name of the country, must be in the english dipiction of the name;
                  
Disable - Will disable this functionalaty intire0ly, it'll ask for one to use once when starting the loop.''')
            response_contry = input()

        if response_options.casefold() ==  "back".casefold():
            print('exiting ')
            break

        else:
            print("Please Write a valid command!")


if __name__ == "__main__":# Command prompt and time loop
    get_settings()
    print(head)
    while True:
        response_command = input()
        if response_command.casefold() ==  "time_loop".casefold():
            print("getting file location ...")
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

        elif response_command.casefold() == 'google_query'.casefold(): #TODO
                neach = input('Name to query: ')
                location = input('Location to query: ')
                search_for =  str(neach + ' ' +  location)
                total = int(input('Number of places to query: '))

                main_query(search_for, total, location)
                print('file saved at results directory')
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

        elif response_command.casefold() == 'options'.casefold():
                clear()
                options()
                clear()
                print(head)

        elif response_command.casefold() == 'help'.casefold(): #TODO make explanetion of all options, and some advices for google query, like location especification, searching without location will search in your area
                clear()

        else:
                print("Please Write a valid command!")
        
