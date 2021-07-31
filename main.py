from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

path = "C:/Program Files (x86)/chromedriver.exe"
PAGE_URL = "https://sede.administracionespublicas.gob.es/icpplustieb/index.html"
driver = webdriver.Chrome(path)

class Customer:
    doc_value = 'Y1234567M'
    name = 'Forename Surname'
    year = '01/01/2020'


def entar(element_id, sending_keys):
    if element_id == '.mf-msg__info':
        try:
            # print(f'trying to find msg__info " {element_id} "')
            WebDriverWait(driver, 2).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".mf-msg__info"), sending_keys))
        except TimeoutException:
            print("APPOINTMENT FOUND")
            while True:
                print('APPOINTMENT FOUND')
        if sending_keys == 'al Captcha del servicio':
            return
    elif element_id == 'form' or element_id == 'tramiteGrupo[0]':
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, element_id)))
        except TimeoutException:
            print("Failed to load a page")
            quit()
        select = Select(driver.find_element_by_id(element_id))
        select.select_by_visible_text(sending_keys)
        for _ in range(50):
            try:
                action = driver.find_element_by_id(element_id)
                action.send_keys(sending_keys)
                break
            except ElementNotInteractableException:
                # logging.error('element not interactable, browser load time is to high, trying again...')
                continue
    else:
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, element_id)))
        except TimeoutException:
            print("Failed to load a page")
            quit()
        for _ in range(50):
            try:
                action = driver.find_element_by_id(element_id)
                action.send_keys(sending_keys)
                break
            except ElementNotInteractableException:
                # logging.error('element not interactable, browser load time is to high, trying again...')
                continue

atmp_numb = 0
#CYCLING THE PROCESS
cycle = True
while cycle:
    cycle = False

    #OPEN PAGE
    driver.get(PAGE_URL)

    entar('form','Madrid')
        # PRESSING ACCEPTAR
    entar('btnAceptar', (Keys.ENTER))

    entar('tramiteGrupo[0]', 'ASILO-OFICINA DE ASILO Y REFUGIO."nueva normalidad” Expedición/Renovación Documentos.C/ Pradillo 40')

    entar('btnAceptar', (Keys.ENTER))

        #1 PRESSING ENTAR BUTTON
    entar('btnEntrar', (Keys.ENTER))

    entar('txtIdCitado', (Customer.doc_value, Keys.TAB, Customer.name, Keys.TAB, Customer.year))

        #3 PRESSING ACCEPTAR BUTTON
    entar('btnEnviar', (Keys.ENTER))

        #4 REQUESTING AN APPOINTMENT(PRESSING SOLICITOR CITA BUTTON)
    entar('btnEnviar', (Keys.ENTER))

        #5 CHECKING FOR APPOINTMENTS
    entar('.mf-msg__info', 'En este momento no hay citas disponibles')

    atmp_numb += 1
    print(f'ATTEMPT: {str(atmp_numb)}. NO LUCK... TRYING AGAIN\n')
    cycle = True
