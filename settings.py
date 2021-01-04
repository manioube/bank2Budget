from dotenv import load_dotenv
load_dotenv()
import os

def o(x):
    # return (os.getenv(x)) if it exists, or raise an Exception otherwise
    r = os.getenv(x)
    if r:
        return r
    else:
        raise Exception('UNKNOWN PARAMETER: environment parameter not set. Set it in `.env` file, or like so: os.environ[foo]="bar".')

try:
    YNAB = {
            'APIKEY': o("ynab_APIkey"),
            'BUDGETID': o("ynab_budgetId"),
            'BANKACCOUNTID': o("ynab_bankAccountId"),
    }
except:
    pass

try:
    TRANSFERWISE = {
        'API_TRANSFERWISE':o("transferwise_api_key"),
        'PROFILE_ID':o("transferwise_profile_id"),
        'ACCOUNT_ID':o("transferwise_account_id"),
    }
except:
    pass

try:
    ING = {
        'ACCOUNT':o("ing_account"),
        'DOB': o("ing_dob"),
        'CODE': o("ing_code")
    }
except:
    pass
