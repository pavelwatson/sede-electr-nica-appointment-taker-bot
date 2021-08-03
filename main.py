import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, UnexpectedAlertPresentException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import telegram_send

path = "C:/Program Files (x86)/chromedriver.exe"
PAGE_URL = "https://sede.administracionespublicas.gob.es"


def return_operation(key):
    """returns an operation string for selecting it in main cycle"""
    return {
        'refugee_documents': 'ASILO-OFICINA DE ASILO Y REFUGIO."nueva normalidad” Expedición/Renovación Documentos.C/ Pradillo 40',
        'fingerprinting':    'POLICIA-TOMA DE HUELLAS (EXPEDICIÓN DE TARJETA) Y RENOVACIÓN DE TARJETA DE LARGA DURACIÓN'
    }[key]


class Customer:
    doc_value = 'Y1234567M'
    name = 'Forename Surname'
    year = '01/01/2020'
    province = 'Madrid',
    operation = return_operation('refugee_documents')


def return_web_element(key):
    """returns an element id for web page interaction"""
    return {
        'tasks':       (By.XPATH, '//*[@id="mainWindow"]/div[2]/section[1]/div/ul/li[7]/a'),
        'appoinments': (By.XPATH, '//*[@id="mainWindow"]/div[2]/div/section/div[2]/ul/li/ul/li[1]/div[1]/p/a'),
        'submit':      (By.ID, 'submit'),
        'provinces':   (By.ID, 'form'),
        'aceptar':     (By.ID, 'btnAceptar'),
        'operation':   (By.ID, 'tramiteGrupo[0]'),
        'entrar':      (By.ID, 'btnEntrar'),
        'form':        (By.ID, 'txtIdCitado'),
        'enviar':      (By.ID, 'btnEnviar'),
        'consultar':   (By.ID, 'btnConsultar'),
        'salir':       (By.ID, 'btnSalir'),
        'appointment': (By.ID, 'btnSiguiente'),
        'country':     (By.ID, 'txtPaisNac'),
        'captcha':     (By.ID, 'btnSubmit'),
        'login':       (By.ID, 'Frm_Username'),
        'router_tab':  (By.ID, 'mmManager'),
        'manage_tab':  (By.ID, 'smSysMgr'),
        'reboot':      (By.ID, 'Submit1')
    }[key]


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


def fill_form(Customer):
    if Customer.operation == return_operation('refugee_documents'):
        action(return_web_element('form'), (Customer.doc_value, Keys.TAB, Customer.name, Keys.TAB, Customer.year))
    elif Customer.operation == return_operation('fingerprinting'):
        action(return_web_element('form'), (Customer.doc_value, Keys.TAB, Customer.name))
        action(return_web_element('country'), 'UCRANIA')
    action(return_web_element('enviar'))


def reboot_router():
    ### reboot router ###
    pass


def cycle(Customer, path):
    global driver
    driver = webdriver.Chrome(path)

    atmp_numb = 0
    while True:
        try:
            prepare_page()

            # choosing a province
            action(return_web_element('provinces'), Customer.province)
            action(return_web_element('aceptar'))

            # choosing an operation
            action(return_web_element('operation'), Customer.operation)
            action(return_web_element('aceptar'))
            action(return_web_element('entrar'))

            # filling a form
            fill_form(Customer)

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


cycle(Customer, path)