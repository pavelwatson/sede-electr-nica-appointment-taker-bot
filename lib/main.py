"""Module with functions for performing actions on a web page and their supporting functions"""

import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import telegram_send

from main.data import web_elements, operations

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


def action(elem, keys=Keys.ENTER, next_elem=''):
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
    action(return_web_element('tasks'), Keys.ENTER)
    action(return_web_element('appoinments'), Keys.ENTER)
    action(return_web_element('submit'), Keys.ENTER)


def captcha_validation_check():
    try:
        wait_elem(return_web_element('captcha'), 2)
    except TimeoutException:
        return
    return True


def appointment_check():
    """CHECKING AN APPOINTMENT"""
    wait_elem(return_web_element('appointment'), 2)
    return True


def fill_form(customer):
    if customer.operation == return_operation('refugee_documents'):
        action(return_web_element('form'), (customer.doc_value, Keys.TAB, customer.name, Keys.TAB, customer.year))
    elif customer.operation == return_operation('fingerprinting'):
        action(return_web_element('form'), (customer.doc_value, Keys.TAB, customer.name))
        action(return_web_element('country'), 'UCRANIA')
    action(return_web_element('enviar'))


def reboot_router():
    ### reboot router ###
    pass


def cycle(customer, path):
    global driver
    driver = webdriver.Chrome(path)

    atmp_numb = 0
    while True:
        try:
            prepare_page()

            # choosing a province
            action(return_web_element('provinces'), customer.province)
            action(return_web_element('aceptar'))

            # choosing an operation
            action(return_web_element('operation'), customer.operation)
            action(return_web_element('aceptar'))
            action(return_web_element('entrar'))

            # filling a form
            fill_form(customer)

            # checking captcha validation
            if captcha_validation_check():
                reboot_router()
                print('CAPTCHA VALIDATION ERROR, REBOOTING THE ROUTER')
                time.sleep(240)
                continue
            time.sleep(100)
            # trying to take an appointment
            action(return_web_element('enviar'))

            # checking if appointment is available
            if appointment_check():
                while True:  # if so, spams the user about it.
                    telegram_send.send(messages=["Appointment found"])

        except TimeoutException:
            atmp_numb += 1
            print(f'ATTEMPT: {str(atmp_numb)}. NO LUCK... TRYING AGAIN')
            continue
