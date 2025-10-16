import requests
from Products.models import Supplier

API_URL = "http://3.226.223.190"

def get_suppliers():
    response = requests.get(f"{API_URL}/api/suppliers")
    suppliers_list = []
    if response.status_code == 200:
        data = response.json()
        for item in data:
            supplier = Supplier(
                id=item.get("id"),
                bussiness_name=item.get("bussiness_name"),
                rut=item.get("rut"),
                email=item.get("email"),
                phone=item.get("phone"),
                trade_terms=item.get("trade_terms")
            )
            suppliers_list.append(supplier)
    else:
        print("FALLOOOOOOOOOOOOOOOO")
    return suppliers_list