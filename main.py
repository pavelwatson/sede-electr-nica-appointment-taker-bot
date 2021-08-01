import random
import time
import os
import random

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, UnexpectedAlertPresentException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import telegram_send

path = "C:/Program Files (x86)/chromedriver.exe"
PAGE_URL = "https://sede.administracionespublicas.gob.es"
driver = webdriver.Chrome(path)

class Customer:
    doc_value = 'Y1234567M'
    name = 'Forename Surname'
    year = '01/01/2020'


#################       MAIN FUNCTIONS         ###########################################
def action(elem, keys, next_elem=''):
    """LOOKING FOR ELEMENT, PERFORMING IT AND CHECK IF IT WAS SUCCESFULL"""
    if wait_for_element(elem) or press_button(elem, keys, next_elem):
        return True
    # time.sleep(random.uniform(0.1, 2))


def wait_for_element(elem):
    """WAITING FOR ELEMENT TO APPEAR ON A PAGE"""
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(elem)
            )
    except TimeoutException:
        if fail():
            return True
    except UnexpectedAlertPresentException:
        if fail():
            return True


def press_button(elem, keys, next_elem):
    """TRYING TO PRESS BUTTON 50 TIMES"""
    for i in range(50):
        try:
            action = driver.find_element(*elem)
            action.send_keys(keys)
            if check_the_page(next_elem):
                return
        except ElementNotInteractableException:
            continue
        except NoSuchElementException:
            captcha = True
            fail(captcha)
            return True
        except UnexpectedAlertPresentException:
            if fail():
                return True
    if fail():
        return True


def check_the_page(next_elem):
    """CHECKING IF PAGE HAS BEEN PASSED"""
    if next_elem:
        try:
            WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.ID, next_elem))
                        )
            return True
        except TimeoutException:
            return False
    return True


def fail(captcha=''):
    """RESTARTING THE CYCLE, AFTER FUNCTION FAILS"""
    if captcha:
        # restart()
        print('CAPTCHA VALIDATION HAS FAILED')
        for i in range(10):
            os.system('wsay "CAPTCHA VALIDATION HAS FAILED"')

    else:
        print("Failed to load")
        for i in range(5):
            os.system('wsay "FAIL"')

    open_page = True
    return True



def restart():
    ### restsart router ###
    pass


def appointment_check(message):
    """CHECKING APPOINTMENT"""
    try:
        WebDriverWait(driver, 2).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".mf-msg__info"), message)
            )
    except TimeoutException:
        print("APPOINTMENT FOUND")
        while True:
            os.system('wsay "RETARD ALERT"')
            telegram_send.send(messages=["Appointment found"])

    action(
        (By.ID, 'btnSalir'),
        Keys.ENTER,
        'form'
    )
    time.sleep(random.uniform(10, 20))

atmp_numb = 0
#CYCLING THE PROCESS
cycle = True
open_page = True
while cycle:
    while open_page:
        
        #OPEN PAGE
        driver.get(PAGE_URL)
        action((By.XPATH, '//*[@id="mainWindow"]/div[2]/section[1]/div/ul/li[7]/a'), Keys.ENTER)
        action((By.XPATH, '//*[@id="mainWindow"]/div[2]/div/section/div[2]/ul/li/ul/li[1]/div[1]/p/a'), Keys.ENTER)
        action((By.ID, 'submit'), Keys.ENTER)
        open_page = False

    if action(
        (By.ID, 'form'),
        'Madrid'
    ):
        open_page = True
        continue

    wait_for_element((By.ID, 'form'))
    if action(
        (By.ID, 'btnAceptar'),
        Keys.ENTER,
        'tramiteGrupo[0]'
    ):
        open_page = True
        continue

    if action(
        (By.ID, 'tramiteGrupo[0]'),
        'ASILO-OFICINA DE ASILO Y REFUGIO."nueva normalidad” Expedición/Renovación Documentos.C/ Pradillo 40'
    ):
        open_page = True
        continue

    wait_for_element((By.ID, 'tramiteGrupo[0]'))
    if action(
        (By.ID, 'btnAceptar'),
        Keys.ENTER,
        'btnEntrar'
    ):
        open_page = True
        continue

    if action(
        (By.ID, 'btnEntrar'),
        Keys.ENTER,
        'txtIdCitado'
    ):
        open_page = True
        continue
    wait_for_element((By.ID, 'txtIdCitado'))
    if action(
        (By.ID, 'txtIdCitado'),
        (Customer.doc_value, Keys.TAB, Customer.name, Keys.TAB, Customer.year),
    ):
        open_page = True
        continue

    if action(
        (By.ID, 'btnEnviar'),
        Keys.ENTER,
        'btnConsultar'
    ):
        open_page = True
        continue

    if wait_for_element((By.ID, 'btnConsultar')):
        open_page = True
        continue
    if action(
        (By.ID, 'btnEnviar'),
        Keys.ENTER,
        'btnSalir'
    ):
        open_page = True
        continue

    appointment_check('En este momento no hay citas disponibles')

    atmp_numb += 1
    print(f'ATTEMPT: {str(atmp_numb)}. NO LUCK... TRYING AGAIN')
