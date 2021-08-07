"""Module with functions for performing actions on a web page and their supporting functions"""

import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import telegram_send

from lib.data import web_elements, operations

PAGE_URL = "https://sede.administracionespublicas.gob.es"


def wait_elem(elem, delay=30):
    """waits for elem element to appear on a page"""
    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located(elem)
        )


def perform_elem(elem, keys):
    """performs keys on element"""
    for i in range(50):
        try:
            element = driver.find_element(*elem)
            element.send_keys(keys)
            break
        except ElementNotInteractableException:
            continue


def action(elem, keys=Keys.ENTER):
    """
    waits for elem element to appear on a page
    performs keys on element
    Check if it was succefull, by waiting for elem to appear on a next page
    """
    wait_elem(elem)
    perform_elem(elem, keys)


def prepare_page():
    """opens PAGE_URL and then setups the page for cycling """
    driver.get(PAGE_URL)
    action(web_elements['tasks'], Keys.ENTER)
    action(web_elements['appoinments'], Keys.ENTER)
    action(web_elements['submit'], Keys.ENTER)


def captcha_validation_check():
    """if Captcha Error has appeared return True, else None"""
    try:
        wait_elem(web_elements['captcha'], 2)
    except TimeoutException:
        return

    return True


def fill_form(customer):
    if operations[customer.operation] == operations['refugee_documents']:
        action(web_elements['form'], (customer.doc_value, Keys.TAB, customer.name, Keys.TAB, customer.year))
    elif operations[customer.operation] == operations['fingerprinting']:
        action(web_elements['form'], (customer.doc_value, Keys.TAB, customer.name))
        action(web_elements['country'], 'UCRANIA')
    action(web_elements['enviar'])


def reboot_router():
    ### reboot router ###
    pass


def main(customer, path):
    global driver
    driver = webdriver.Chrome(path)
    atmp_numb = 0
    while True:
        prepare_page()

        # choosing a province
        action(web_elements['provinces'], customer.province)
        action(web_elements['aceptar'])

        # choosing an operation
        action(web_elements['operation'], operations[customer.operation])
        action(web_elements['aceptar'])
        action(web_elements['entrar'])

        # filling a form
        fill_form(customer)

        # checking captcha validation
        if captcha_validation_check():
            reboot_router()
            print('CAPTCHA VALIDATION ERROR, REBOOTING THE ROUTER')
            time.sleep(240)
            continue

        # trying to take an appointment
        action(web_elements['enviar'])

        # if message "No Citas at the moment" appears, then continue
        no_citas = driver.find_elements(*web_elements['no_citas'])
        if no_citas:
            atmp_numb += 1
            print(f'ATTEMPT: {str(atmp_numb)}. NO LUCK... TRYING AGAIN')
            continue

        # if there is a cita notify a user
        while True:
            telegram_send.send(messages=["Appointment found"])
