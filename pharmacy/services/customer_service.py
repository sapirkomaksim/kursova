# services/customer_service.py

from repositories.customer_repo import CustomerRepository


class CustomerService:

    def __init__(self):
        self.repo = CustomerRepository()

    def create_customer(self, full_name, phone):
        return self.repo.add(full_name, phone)

    def list_customers(self):
        return self.repo.list_all()