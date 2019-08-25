import time
import os
import random
from selenium import webdriver
from parsel import Selector
import pandas as pd
import datetime
import urllib.request
from selenium.common.exceptions import NoSuchElementException


def link_scraper(browser):
    df = pd.read_csv('carrot.csv')
    url_list = df["list_of_companies"].tolist()
    name_list = df["list_of_company_names"].tolist()
    Selector(text=browser.page_source)
    time.sleep(random.randint(1, 5))
    # Print list
    list_of_employee_links = []
    list_of_employee_src_links = []
    list_of_actor_names = []
    for i, url in enumerate(url_list):
        root_url = "https://www.linkedin.com"
        browser.get(url)
        companyname = name_list[i].replace(" ","_")
        file_name = companyname + ".csv"
        dirname = r'C:/Users/Owner/PycharmProjects/EmployeeLinkCollector/ScrapedData/' + companyname + '/'
        filepath = dirname + file_name
        image_dir = r'C:/Users/Owner/PycharmProjects/EmployeeLinkCollector/ScrapedData/' + companyname + '/'
        try:
            os.mkdir(dirname)
        except OSError:
            if os.path.isdir(dirname):
                pass
            else:
                raise

        time.sleep(random.randint(1, 4))
        # # Saving Logo
        # # company_logo_src = sel.xpath('//*[@class="lazy-image org-top-card-primary-content__logo Elevation-0dp loaded"]/@src').get()
        # # print(company_logo_src)
        # # full_file_name_and_path_of_logo = os.path.join(image_dir, companyname + ".png")
        # # urllib.request.urlretrieve(company_logo_src, full_file_name_and_path_of_logo)
        try:
            browser.find_element_by_xpath('//span[@class="v-align-middle"]').click()
        except NoSuchElementException:
            pass

        time.sleep(random.randint(1, 5))

        # Collecting Names, images and hreftags = employee links, then save the images with names.
        # Along with employee links to excel file.
        try:
            condition = True

            while condition:
                time.sleep(random.randint(1, 3))
                sel = Selector(text=browser.page_source)
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Selecting the names of all visible actors on given page.
                actor_names = sel.xpath('//span[@class="name actor-name"]/text()').getall()
                # Selecting the hreftags of all visible actors on given page.
                hreftags = sel.xpath('//div[@class="search-result__image-wrapper"]//a[@class="search-result__result-link ember-view"]/@href').getall()
                # Concatenate root_urk with all visible hreftags.
                for x_href in hreftags:
                    employee_links = root_url + x_href
                    list_of_employee_links.append(employee_links)
                # Selecting all images of all visible actors on given page.
                imgs = sel.xpath('//img[@class="lazy-image ivm-view-attr__img--centered  EntityPhoto-circle-4 presence-entity__image EntityPhoto-circle-4 loaded"]/@src').getall()
                # Opening each image url and storing the images in the a given project directory.
                for index, x_link in enumerate(imgs):
                    x_name = actor_names[index]
                    full_file_name_and_path = os.path.join(image_dir, x_name + ".png")
                    urllib.request.urlretrieve(x_link, full_file_name_and_path)
                    list_of_actor_names.append(x_name)
                    list_of_employee_src_links.append(x_link)
                # Next Button
                next_button = browser.find_element_by_xpath('//button[@class="artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view"]')
                if next_button:
                    time.sleep(random.randint(2, 4))
                    next_button.click()
                else:
                    condition = False
        except:
            pass
    data_file_writer = pd.DataFrame(list_of_employee_links, columns=['URLS'])
    data_file_writer.to_csv(filepath, sep=',', index=False, encoding='utf-8')
    print('Actor Names: ', list_of_actor_names)
    print('\n')
    print('List of Employees: ', list_of_employee_links)
    print('\n')


def main():
    browser = webdriver.Firefox() #(options=options)
    print('\n')
    print('Activating: Headless Mode!')
    print('\n')
    browser.get("https://linkedin.com/uas/login")
    email_element = browser.find_element_by_id("username")
    email_element.send_keys("johndowteam@gmail.com")
    pass_element = browser.find_element_by_id("password")
    pass_element.send_keys("password123#")
    pass_element.submit()
    print('\n')
    print(datetime.datetime.now())
    print('\n')
    print("Login Success!")
    print('\n')
    time.sleep(3)
    print('\n')

    link_scraper(browser)

    #print('activating ViewBot!')
    #os.open('ViewBot.py')

    # replace with 'clear' for Unix type system.
    os.system('cls')
    browser.close()


if __name__ == "__main__":
    main()
