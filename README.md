# bank2BudgettingApp

## Description

This package will download bank transactions from a bank website, then upload them to a budgetting app.

Example provided works with ING and YNAB.

## Pre-requisite

- Python 3
- pip3

## Using with the command line

1. place sensitive data in `.env` file like so:

`ynab_APIkey = '...'  # api_key is a token you get in Developer settings
ynab_budgetId = '...'
ynab_bankAccountId = '...'
ing_account = '...'
ing_dob = '...'
ing_code = '...'`

Then run from console:

`./run.py getdata -b ing push2budgetapp -budgetapp ynab`

## Note

The app will push data to YNAB, until it encounters a conflict error (transaction already imported)

## Source

https://github.com/tducret/ingdirect-python (French only)