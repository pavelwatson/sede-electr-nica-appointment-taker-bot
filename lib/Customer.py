"""module that describes a customer profile for using it on a web"""


class CustomerProfile:
    """class that describes a client"""

    def __init__(self, doc_value, name, year, province, operation):
        """initialising client information to fill the page with"""
        self.doc_value = doc_value
        self.name = name
        self.year = year
        self.province = province
        self.operation = operation
