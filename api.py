import requests

url = "https://reqres.in/api/users"


response = requests.get(url)

if response.status_code == 200:
	data = response.json()
	for user in data["data"]:
		print ("ID:",user["id"])
		print ("EMAİL:",user["email"])
		print ("First Name:",user["first_name"])
		print ("Last Name:",user["last_name"])
		print ("Avatar:",user["avatar"])
		print ("\n")
else:
	print ("Hata! Durum Kodu:",response.status_code)
