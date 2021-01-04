#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://github.com/pallets/click/blob/master/examples/imagepipe/imagepipe.py

# https://click.palletsprojects.com/en/7.x/commands/#multi-command-chaining

# https://dbader.org/blog/mastering-click-advanced-python-command-line-apps

# https://stackoverflow.com/questions/58579837/changing-function-code-using-a-decorator-and-execute-it-with-eval

import click
from functools import update_wrapper
import importlib

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
            yield (data)

        elif bank_name == "transferwise":
            click.echo("will do Transferwise-specific actions")
            transferwise = importlib.import_module('banks.transferwise')
            data = transferwise.main()
            yield data

        else:
            yield (
                {
                    "bank": bank_name,
                    "retour_synthese_comptes": None,
                    "retour_ops": None,
                    "message": "bank is other than ING or Transferwise, data retrieval not yet implemented..."
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

            elif d[1]["bank"] == "transferwise":
                print(d)
                click.echo(d[1]["message"])
                y_instance.JSON_OPS_2_YNAB(d[1]["retour_ops"])

            else:
                click.echo(d[1]["message"])
            yield d


    click.echo("all data has been pushed to budget app:" + budgetapp)

    return ("data was pushed to " + budgetapp)


if __name__ == '__main__':
    cli()