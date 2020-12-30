#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://github.com/pallets/click/blob/master/examples/imagepipe/imagepipe.py

# https://click.palletsprojects.com/en/7.x/commands/#multi-command-chaining

# https://dbader.org/blog/mastering-click-advanced-python-command-line-apps

# https://stackoverflow.com/questions/58579837/changing-function-code-using-a-decorator-and-execute-it-with-eval

import click
from functools import update_wrapper
import importlib
import settings

# run --bank <bankName> --data <dataList> --save <fileName> --convert <srcType, tgtType> --budget <budgetAppName>
# simple command to start with: --bank ing --data ops --budget YNAB

@click.group(chain=True)

def cli():
    pass

@cli.resultcallback()

def process_commands(processors):
    """This result callback is invoked with an iterable of all the chained
    subcommands.  As in this example each subcommand returns a function
    we can chain them together to feed one into the other, similar to how
    a pipe on unix works.
    """
    # Start with an empty iterable.
    stream = ()

    # Pipe it through all stream processors.
    for processor in processors:
        stream = processor(stream)

    # Evaluate the stream and throw away the items.
    for _ in stream:
        pass

def processor(f):
    """Helper decorator to rewrite a function so that it returns another
    function from it.
    """

    def new_func(*args, **kwargs):
        def processor(stream):
            return f(stream, *args, **kwargs)

        return processor

    return update_wrapper(new_func, f)

def generator(f):
    """Similar to the :func:`processor` but passes through old values
    unchanged and does not pass through the values as parameter.
    """

    @processor
    def new_func(stream, *args, **kwargs):
        yield from stream
        yield from f(*args, **kwargs)

    return update_wrapper(new_func, f)

"""

The `getdata` command takes multiple bank/aggregator values, like so: `getdata -b ing -b socgen -b transferwise`

It outputs a generator

"""


@cli.command("getdata")
@click.option(
    "-b",
    "--bank",
    "bank",
    # default="ing",
    type=str,
    multiple=True,
    # help="will connect to the bank and get specified data",
    # show_default=True,
)
@generator
def getdata_cmd(bank):
    """Saves all processed images to a series of files."""
    # click.echo("will get data from bank:" + bank) # + b
    # # return bank
    # yield ("this is the data I got from: " + bank)
    for b in enumerate(bank):
        bank_name = b[1]
        click.echo("getting data from bank:" + bank_name)

        if bank_name == "ing":
            click.echo("will do ING-specific actions")
            ing = importlib.import_module('banks.ing')
            data = ing.main()
            # data = [{'id': '7586', 'effectiveDate': '2020-11-11', 'accountingDate': '2020-11-11', 'detail': 'VIREMENT RECU MME ADELINE TUAL 40005037581 LOYER', 'amount': 500.0, 'transcodeNeedCustomerAction': False, 'type': 'TRANSFER', 'isOldBankCode': False, 'sameMonthAsPrevious': False, 'sameDateAsPrevious': False, 'sameDateAsNext': True}, {'id': '7583', 'effectiveDate': '2020-11-11', 'accountingDate': '2020-11-11', 'detail': 'VIREMENT SEPA EMIS VERS  00040403391', 'amount': -70.0, 'transcodeNeedCustomerAction': False, 'type': 'TRANSFER', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': True, 'sameDateAsNext': False}, {'id': '7581', 'effectiveDate': '2020-11-10', 'accountingDate': '2020-11-10', 'detail': 'PAIEMENT PAR CARTE 09/11/2020 SAS BERGOULI', 'amount': -2.0, 'transcodeNeedCustomerAction': False, 'type': 'PURCHASE_CARD', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': False, 'sameDateAsNext': False}, {'id': '7579', 'effectiveDate': '2020-11-09', 'accountingDate': '2020-11-09', 'detail': "PAIEMENT D'UN CHÃˆQUE 4729474", 'amount': -529.0, 'transcodeNeedCustomerAction': False, 'type': 'CHECK', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': False, 'sameDateAsNext': True}, {'id': '7577', 'effectiveDate': '2020-11-09', 'accountingDate': '2020-11-09', 'detail': 'PAIEMENT PAR CARTE 08/11/2020 QUITOQUE', 'amount': -64.9, 'transcodeNeedCustomerAction': False, 'type': 'PURCHASE_CARD', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': True, 'sameDateAsNext': False}, {'id': '7572', 'effectiveDate': '2020-11-07', 'accountingDate': '2020-11-07', 'detail': 'PAIEMENT PAR CARTE 06/11/2020 AMZN MKTP FR*M78JQ6354', 'amount': -3.22, 'transcodeNeedCustomerAction': False, 'type': 'PURCHASE_CARD', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': False, 'sameDateAsNext': False}, {'id': '7568', 'effectiveDate': '2020-11-05', 'accountingDate': '2020-11-05', 'detail': 'VIREMENT SEPA RECU DRFIP OCCITANIE ET HTE G /INV/PEK5T01 27.10.2020', 'amount': 81.0, 'transcodeNeedCustomerAction': False, 'type': 'TRANSFER', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': False, 'sameDateAsNext': True}, {'id': '7566', 'effectiveDate': '2020-11-05', 'accountingDate': '2020-11-05', 'detail': 'VIREMENT SEPA RECU CAF DES PA VIRINST XPXREFERENCE  010748770      ME    0535857ZBEKAERT     102020ME', 'amount': 49.49, 'transcodeNeedCustomerAction': False, 'type': 'TRANSFER', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': True, 'sameDateAsNext': True}, {'id': '7564', 'effectiveDate': '2020-11-05', 'accountingDate': '2020-11-05', 'detail': 'PRLV SEPA SNCTA : FR88ZZZ188352 335444 DE SNCTA : 335444 FR88ZZZ188352', 'amount': -35.0, 'transcodeNeedCustomerAction': False, 'type': 'SEPA_DEBIT', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': True, 'sameDateAsNext': True}, {'id': '7562', 'effectiveDate': '2020-11-05', 'accountingDate': '2020-11-05', 'detail': 'PRLV SEPA SAS MULTI IMPACT : FR10ZZZ504715 EG2017-000268320-01 DE SAS MULTI IMPACT : EG2017-000268320-01 FR10ZZZ504715', 'amount': -30.32, 'transcodeNeedCustomerAction': False, 'type': 'SEPA_DEBIT', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': True, 'sameDateAsNext': True}, {'id': '7560', 'effectiveDate': '2020-11-05', 'accountingDate': '2020-11-05', 'detail': 'PRLV SEPA SAS MULTI IMPACT : FR10ZZZ504715 EG2017-000268323-01 DE SAS MULTI IMPACT : EG2017-000268323-01 FR10ZZZ504715', 'amount': -37.83, 'transcodeNeedCustomerAction': False, 'type': 'SEPA_DEBIT', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': True, 'sameDateAsNext': True}, {'id': '7558', 'effectiveDate': '2020-11-05', 'accountingDate': '2020-11-05', 'detail': 'PRLV SEPA TOTAL DIRECT ENERGIE : FR03ZZZ488157 DEMP003220824 DE TOTAL DIRECT ENERGIE : DEMP003220824 FR03ZZZ488157', 'amount': -111.0, 'transcodeNeedCustomerAction': False, 'type': 'SEPA_DEBIT', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': True, 'sameDateAsNext': True}, {'id': '7556', 'effectiveDate': '2020-11-05', 'accountingDate': '2020-11-05', 'detail': 'PRLV SEPA TOTAL DIRECT ENERGIE : FR03ZZZ488157 DEMP003220824 DE TOTAL DIRECT ENERGIE : DEMP003220824 FR03ZZZ488157', 'amount': -234.0, 'transcodeNeedCustomerAction': False, 'type': 'SEPA_DEBIT', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': True, 'sameDateAsNext': True}, {'id': '7554', 'effectiveDate': '2020-11-05', 'accountingDate': '2020-11-05', 'detail': 'PRLV SEPA ING BANK N.V. : FR11IMM638266 PERING900022107670001 DE ING BANK N.V. : PERING900022107670001 FR11IMM638266', 'amount': -1534.02, 'transcodeNeedCustomerAction': False, 'type': 'SEPA_DEBIT', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': True, 'sameDateAsNext': True}, {'id': '7552', 'effectiveDate': '2020-11-05', 'accountingDate': '2020-11-05', 'detail': 'PRLV SEPA FREE TELECOM : FR83ZZZ459654 30860149 DE FREE TELECOM : 30860149 FR83ZZZ459654', 'amount': -39.99, 'transcodeNeedCustomerAction': False, 'type': 'SEPA_DEBIT', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': True, 'sameDateAsNext': False}, {'id': '7550', 'effectiveDate': '2020-11-04', 'accountingDate': '2020-11-04', 'detail': 'PAIEMENT PAR CARTE 22/10/2020 AUCHAN B2C DRIVE', 'amount': -115.38, 'transcodeNeedCustomerAction': False, 'type': 'PURCHASE_CARD', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': False, 'sameDateAsNext': True}, {'id': '7548', 'effectiveDate': '2020-11-04', 'accountingDate': '2020-11-04', 'detail': 'PAIEMENT PAR CARTE 03/11/2020 BOULANGERIE DU M', 'amount': -5.5, 'transcodeNeedCustomerAction': False, 'type': 'PURCHASE_CARD', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': True, 'sameDateAsNext': False}, {'id': '7545', 'effectiveDate': '2020-11-03', 'accountingDate': '2020-11-03', 'detail': 'PAIEMENT PAR CARTE 02/11/2020 AUCHAN B2C DRIVE', 'amount': -109.91, 'transcodeNeedCustomerAction': False, 'type': 'PURCHASE_CARD', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': False, 'sameDateAsNext': False}, {'id': '7542', 'effectiveDate': '2020-11-02', 'accountingDate': '2020-11-02', 'detail': 'VIREMENT SEPA RECU PHARMACIE DE BENEJACQ', 'amount': 3000.0, 'transcodeNeedCustomerAction': False, 'type': 'TRANSFER', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': False, 'sameDateAsNext': True}, {'id': '7540', 'effectiveDate': '2020-11-02', 'accountingDate': '2020-11-02', 'detail': 'PAIEMENT PAR CARTE 01/11/2020 AMZN MKTP FR*MC7KB5YQ4', 'amount': -52.99, 'transcodeNeedCustomerAction': False, 'type': 'PURCHASE_CARD', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': True, 'sameDateAsNext': True}, {'id': '7537', 'effectiveDate': '2020-11-02', 'accountingDate': '2020-11-02', 'detail': 'PAIEMENT PAR CARTE 31/10/2020 QUITOQUE', 'amount': -59.0, 'transcodeNeedCustomerAction': False, 'type': 'PURCHASE_CARD', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': True, 'sameDateAsNext': True}, {'id': '7531', 'effectiveDate': '2020-11-02', 'accountingDate': '2020-11-02', 'detail': 'VIREMENT SEPA EMIS VERS  BE98967158568993 PAUL', 'amount': -1250.0, 'transcodeNeedCustomerAction': False, 'type': 'TRANSFER', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': True, 'sameDateAsNext': True}, {'id': '7529', 'effectiveDate': '2020-11-02', 'accountingDate': '2020-11-02', 'detail': 'VIREMENT SEPA EMIS VERS  00056003107 PTZ', 'amount': -124.5, 'transcodeNeedCustomerAction': False, 'type': 'TRANSFER', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': True, 'sameDateAsNext': False}, {'id': '7525', 'effectiveDate': '2020-10-30', 'accountingDate': '2020-10-30', 'detail': 'VIREMENT EMIS VERS M. EMMANUEL BEKAERT OU MME GAELLE BEKAERT 10013514566', 'amount': -1004.16, 'transcodeNeedCustomerAction': False, 'type': 'TRANSFER', 'isOldBankCode': False, 'sameMonthAsPrevious': False, 'sameDateAsPrevious': False, 'sameDateAsNext': True}, {'id': '7523', 'effectiveDate': '2020-10-30', 'accountingDate': '2020-10-30', 'detail': 'VIREMENT SEPA EMIS VERS', 'amount': -1553.0, 'transcodeNeedCustomerAction': False, 'type': 'TRANSFER', 'isOldBankCode': False, 'sameMonthAsPrevious': True, 'sameDateAsPrevious': True, 'sameDateAsNext': True}]
            # print("data returned from ING", data.retour_synthese_comptes)
            yield (data)
        else:
            yield (
                {
                    "bank": bank_name,
                    "retour_synthese_comptes": None,
                    "retour_ops": None,
                    "message": "bank is other than ING, data retrieval not yet implemented..."
                }
            )


"""

The `push2budgetapp` command takes a generator of json strings, that contain bank data

It pushes each entry to the relevant budgeting apps

"""

@cli.command("push2budgetapp")
@click.option(
    "-budgetapp",
    "--budgetapp",
    "budgetapp",
    # default="ing",
    type=str,
    # help="will connect to the bank and get specified data",
    # show_default=True,
)
@processor
def push2budgetapp_cmd(data, budgetapp):
    """Saves all processed images to a series of files."""
    # for d in enumerate(data):
    #     click.echo("data:", d)

    click.echo("will now push to budget app:" + budgetapp)

    if(budgetapp == 'ynab'):

        y = importlib.import_module('budgeting_apps.YNAB')
        y_instance = y.Ynab()

        for d in enumerate(data):

            if d[1]["bank"] == "ing":
                click.echo(d[1]["message"])
                y_instance.JSON_OPS_2_YNAB(d[1]["retour_ops"])

            else:
                click.echo(d[1]["message"])
            yield d

    click.echo("all data has been pushed to budget app:" + budgetapp)

    return ("data was pushed to " + budgetapp)


if __name__ == '__main__':
    cli()