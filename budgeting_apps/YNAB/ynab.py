from __future__ import print_function
import ynab
from ynab.rest import ApiException
from pprint import pprint
import json
import itertools
import os

# from urllib.parse import urljoin
# import os
# import sys
# # insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, urljoin(os.getcwd(), 'config'))
# from config import ynabConfig
import settings
configuration = ynab.Configuration()
configuration.api_key['Authorization'] = settings.YNAB['APIKEY'] # api_key is a token you get in Developer settings
# # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
configuration.api_key_prefix['Authorization'] = 'Bearer'
api_instance = ynab.TransactionsApi(ynab.ApiClient(configuration))

class Ynab():

    def sayHello(self):
        print("hello")

    def loadJSONfromFile(self, file): # will load JSON from a JSON file
        with open(file) as f:
            r = json.load(f)
        return r

    def JSON_OPS_2_YNAB(self, src): # will post json bank transactions to YNAB
        for op in itertools.islice(src , 0, 20): # number of transactions that should be posted

            date = op['effectiveDate']
            amount = int(op['amount'] * 1000) # amount is in milliunit of currency
            import_id = op['id'] #"YNAB:" + amount + ":" + date + ":" #[occurrence]
            approved = True
            payee_name =  (op['detail'][:97] + '...') if len(op['detail']) > 99 else op['detail'] # limit to 100 characters

            transaction = ynab.SaveTransactionWrapper(

                    {
                        'account_id': settings.YNAB['BANKACCOUNTID'],
                        'date': date,
                        'amount': amount,
                        'approved': approved,
                        'import_id': import_id,
                        'payee_name': payee_name
                    }

            )

            try:
                # List transactions
                ## api_response = api_instance.get_transactions(budget_id) #, since_date = since_date, type = type

                # see https://github.com/deanmcgregor/ynab-python/blob/master/docs/SaveTransaction.md for info on transactions
                api_response = api_instance.create_transaction(settings.YNAB['BUDGETID'], transaction)
                pprint(api_response)
            except ApiException as e:
                print("Exception when calling TransactionsApi->get_transactions: %s\n" % e)

# script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
# rel_path = "../../path/to/file.json" #<-- relative path to file containing bank transactions
# abs_file_path = os.path.join(script_dir, rel_path)
#
# Ynab.JSON_OPS_2_YNAB ( Ynab.loadJSONfromFile ( abs_file_path ) )




# a transaction example: {
# account_id 	str
# date 	date
# amount 	float 	The transaction amount in milliunits format
# payee_id 	str 	The payee for the transaction. Transfer payees are not permitted and will be ignored if supplied. 	[optional]
# payee_name 	str 	The payee name. If a payee_name value is provided and payee_id is not included or has a null value, payee_name will be used to create or use an existing payee. 	[optional]
# category_id 	str 	The category for the transaction. Split and Credit Card Payment categories are not permitted and will be ignored if supplied. 	[optional]
# memo 	str 		[optional]
# cleared 	str 	The cleared status of the transaction 	[optional]
# approved 	bool 	Whether or not the transaction is approved. If not supplied, transaction will be unapproved by default. 	[optional]
# flag_color 	str 	The transaction flag 	[optional]
# import_id 	str 	If specified for a new transaction, the transaction will be treated as Imported and assigned this import_id. If another transaction on the same account with this same import_id is later attempted to be created, it will be skipped to prevent duplication. Transactions imported through File Based Import or Direct Import and not through the API, are assigned an import_id in the format: 'YNAB:[milliunit_amount]:[iso_date]:[occurrence]'. For example, a transaction dated 2015-12-30 in the amount of -$294.23 USD would have an import_id of 'YNAB:-294230:2015-12-30:1'. If a second transaction on the same account was imported and had the same date and same amount, its import_id would be 'YNAB:-294230:2015-12-30:2'. Using a consistent format will prevent duplicates through Direct Import and File Based Import. If import_id is specified as null, the transaction will be treated as a user entered transaction.
# }