from selenium.webdriver.common.by import By


web_elements = {
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
    'reboot':      (By.ID, 'Submit1'),
    'no_citas':    (By.XPATH, '//*[@id="mainWindow"]/div/div/section/div[2]/form/div[1]/p'),
    'alreadyhave': (By.XPATH, '//*[@id="warning"]/ul/li/p[2]/span/span/font[1]/font'),
    'session_expired': (By.XPATH, '//*[@id="mensajeInfo"]/p[1]/span')
    }


operations = {
    'refugee_documents': 'ASILO-OFICINA DE ASILO Y REFUGIO."nueva normalidad” Expedición/Renovación Documentos.C/ Pradillo 40',
    'fingerprinting':    'POLICIA-TOMA DE HUELLAS (EXPEDICIÓN DE TARJETA) Y RENOVACIÓN DE TARJETA DE LARGA DURACIÓN'
    }
