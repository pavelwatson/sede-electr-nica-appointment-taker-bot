from lib import CustomerProfile, cycle, operation

path = "C:/Program Files (x86)/chromedriver.exe"  # Path for your chrome driver
customer = CustomerProfile(  # fill the customer information
    doc_value='',
    name='',
    year='DD/MM/YYYY',
    province='Madrid',
    operation=operation('refugee_documents')
    )


if __name__ == '__main__':
    cycle(customer, path)
