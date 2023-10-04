from dataclasses import dataclass, asdict, field
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time
from tkinter import * 
from tkinter import filedialog

def open_file_dialog():
    root = Tk()
    root.withdraw()
    root.update()
    file_path = filedialog.askopenfilename()
    root.destroy()

    return file_path

@dataclass
class Business:
    """holds business data
    """
    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None

@dataclass
class BusinessList:
    """holds list of Business objects, 
       and save to both excel and csv
    """
    business_list : list[Business] = field(default_factory=list)
    
    def dataframe(self):
        """transform business_list to pandas dataframe 

        Returns: pandas dataframe
        """
        return pd.json_normalize((asdict(business) for business in self.business_list), sep="_")
    
    def save_to_excel(self, filename):
        """saves pandas dataframe to excel (xlsx) file

        Args:
            filename (str): filename
        """ 
        file_location = open_file_dialog()
        self.dataframe().to_excel(f'{file_location}/{filename}.xlsx', index=False)
    
    def save_to_csv(self, filename):
        """saves pandas dataframe to csv file

        Args:
            filename (str): filename
        """
        print('reached')
        file_location = open_file_dialog()
        self.dataframe().to_csv(f'{file_location}/{filename}.csv', index=False, sep=';')


def main_query(search_for, total, location):
        navegador = webdriver.Chrome()
        navegador.get("https://www.google.com.br/maps")

        time.sleep(3)
        navegador.find_element(By.XPATH, '//*[@id="searchboxinput"]').send_keys(location)
        time.sleep(2)
        navegador.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]').click()
        time.sleep(15)
        navegador.find_element(By.XPATH, '//*[@id="searchbox"]/div[2]/button').click()
        time.sleep(5)

        navegador.find_element(By.XPATH, '//*[@id="searchboxinput"]').send_keys(search_for)
        navegador.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]').click()
        time.sleep(10)

        previously_counted = 0
        while True:
                list_elem = navegador.find_elements(By.CLASS_NAME, 'hfpxzc')

                action = ActionChains(navegador)
                action.move_to_element(list_elem[-1]).perform()
                
                time.sleep(5)
                scroll_origin = ScrollOrigin.from_element(list_elem[-1])
                action.scroll_from_origin(scroll_origin, 0, 1200).perform()
                
                time.sleep(20)
                action.scroll_from_origin(scroll_origin, 0, 250).perform()
                if len(list_elem) >= total:
                    print(f'''Total Scraped: {len(list_elem)}
                          
----------------------------------------------------''')
                    break

                else:
                    if len(list_elem) == previously_counted:
                        print(f'''Arrived at all available
        Total Scraped: {len(list_elem)}
-----------------------------------------------------''')
                        break

                    else:
                        previously_counted = len(list_elem)
                        print(f'Currently Scraped: ', len(list_elem))
        
        business_list = BusinessList()
        
        # scraping
        for x, listing in enumerate(list_elem):
            time.sleep(2)
            if x == 0:
                action_2 = ActionChains(navegador)
                action_2.scroll_to_element(listing).perform()
                action_2.move_to_element(listing).perform()

                time.sleep(2)
                listing.click()
            else:
                integer = x - 1
                scroll_origin = ScrollOrigin.from_element(list_elem[integer])
                action_2 = ActionChains(navegador)
                action_2.scroll_to_element(listing).perform()
                action_2.scroll_from_origin(scroll_origin, 0, 190).perform()
                action_2.scroll_to_element(listing).perform()
                action_2.move_to_element(listing).perform()
                
                time.sleep(2)
                listing.click()

            time.sleep(5)
    
            name_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1'
            #'//h1[contains(@class, "fontHeadlineLarge")]'
            address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
            business = Business()
            try:
                if len(navegador.find_element(By.XPATH, name_xpath).text) > 0:
                    business.name = navegador.find_element(By.XPATH, name_xpath).text
                else:
                    business.name = ''
            except NoSuchElementException:
                    business.name = ''

            try:    
                if len(navegador.find_element(By.XPATH, address_xpath).text) > 0:
                    business.address = navegador.find_element(By.XPATH, address_xpath).text
                else:
                    business.address = ''
            except NoSuchElementException:
                    business.address = ''

            try:        
                if len(navegador.find_element(By.XPATH, website_xpath).text) > 0:
                    business.website = navegador.find_element(By.XPATH, website_xpath).text
                else:
                    business.website = ''
            except NoSuchElementException:
                    business.website = ''

            try:
                if len(navegador.find_element(By.XPATH, phone_number_xpath).text) > 0:
                    business.phone_number = navegador.find_element(By.XPATH, phone_number_xpath).text
                else:
                    business.phone_number = ''
            except NoSuchElementException:
                    business.phone_number = ''

            business_list.business_list.append(business)
        
        updated_string = search_for.replace(" ", "_")
        while True:
            save_str = """Save results to file? options:
Save_excel ; Save_csv ; Exit. """
            response_command = input(save_str)
            if response_command.casefold() == 'save_excel'.casefold():
                print('saving to excel file...')
                business_list.save_to_excel(f'maps_data_{updated_string}')
                print('done')

            if response_command.casefold() == 'save_csv'.casefold():
                print('saving to csv file...')
                business_list.save_to_csv(f'maps_data_{updated_string}')
                print('done')

            if response_command.casefold() == 'exit'.casefold():
                break

            else:
                print('please write a valid command!')


if __name__ == "__main__":
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int)
    args = parser.parse_args()
    
    if args.search:
        search_for = args.search
    else:
        # in case no arguments passed
        # the scraper will search by default for:
        search_for = 'tattoo ireland'
    
    # total number of products to scrape. Default is 10
    if args.total:
        total = args.total
    else:
        total = 20
    '''
    neach = input('Name to query: ')
    location = input('Location to query: ')
    search_for =  str(neach + ' ' +  location)

    total = int(input('Number of places to query: '))
    main_query(search_for, total, location) 
