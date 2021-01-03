import requests
import json
import ynab
import datetime
import os
import settings

# Test your values here:
API_KEY = settings.TRANSFERWISE["API_TRANSFERWISE"]
PROFILE_ID = settings.TRANSFERWISE["PROFILE_ID"]
ACCOUNT_ID = settings.TRANSFERWISE["ACCOUNT_ID"]

def getTransactionData():
	transactions = []
	currencies = ["GBP"]

	# Find last time data was retrieved
	with open(f"{os.getcwd()}/banks/transferwise/last.txt", "r") as f:
		start_date = f.readlines()[0]
	today = datetime.date.today()
	end_date = today.strftime("%Y-%m-%d")

	# Data has already been imported
	if (start_date == str(end_date)) or (start_date == str(today + datetime.timedelta(days=1))):
		print("You have already imported all transactions. Wait at least two days before importing again.")
		quit()

	print(f"Importing transactions between {start_date} and {end_date}")

	# Import all transactions from transferwise
	for currency in currencies:
		url = f"https://api.transferwise.com/v3/profiles/{PROFILE_ID}/borderless-accounts/{ACCOUNT_ID}/statement.json?currency={currency}&intervalStart={start_date}T00:00:00.000Z&intervalEnd={end_date}T23:59:59.999Z&type=COMPACT"
		res = requests.get(url, headers={"Authorization": f"Bearer {API_KEY}"}).content.decode()
		res.join("")
		res = json.loads(res)

		# Put transactions into list
		try:
			for transaction in res["transactions"]:
				transactions.append([float(transaction['amount']['value']), transaction['date'], transaction['amount']['currency'], transaction["referenceNumber"], transaction["details"]["description"]])

		except KeyError:
			print("No transactions to import")
			quit()

	# Format transation for the ynab api
	result_dict = []
	for i, tr in enumerate(transactions):
		tr[1] = tr[1][:10]
		result_dict_temp = {}
		result_dict_temp["account_id"] = 'e78b1943-e129-4a23-b69f-1bb6603585bc'
		result_dict_temp["effectiveDate"] = tr[1]
		result_dict_temp["amount"] = tr[0]
		result_dict_temp["id"] = datetime.datetime.utcnow()
		result_dict_temp["payee_name"] = ""
		result_dict_temp["detail"] = tr[4]
		result_dict_temp["approved"] = True
		result_dict.append(result_dict_temp)

	# Update last time push was done
	with open(f"{os.getcwd()}/banks/transferwise/last.txt", "w") as f:
		f.write(str(datetime.date.today() + datetime.timedelta(days=1)))

	return result_dict

def main():

	transactions = getTransactionData()

	data = {
		"bank" : "transferwise",
		"retour_synthese_comptes": transactions,
		"retour_ops": transactions,
		"message": "data was retrieved from transferwise"
	}
	return data


if __name__ == "__main__":
	main()