from lib import CustomerProfile, cycle, operation

path = "C:/Program Files (x86)/chromedriver.exe"  # Path for your chrome driver

customer = CustomerProfile(  # fill the customer information
    doc_value='Y1234567',
    name='',
    year='DD/MM/YYYY',
    province='Madrid',
    operation=operation('fingerprinting')
    )


cycle(customer, path)
