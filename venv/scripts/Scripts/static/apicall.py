import requests
url='https://frappe.io/api/method/frappe-library?page=2&title=and'
response=requests.get(url)
book_dictionary=response.json()
print(book_dictionary)