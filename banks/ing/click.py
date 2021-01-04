import click

@click.command()
@click.option(
    '--num_client', '-n',
    envvar="ING_NUM_CLIENT",
    type=str,
    help='votre numéro client ING Direct',
    prompt='votre numéro client ING Direct',
    required=True,
)
@click.option(
    '--date_naissance', '-d',
    envvar="ING_DATE_NAISSANCE",
    type=str,
    help='votre date de naissance au format JJMMAAAA (ex: 30121982)',
    prompt='votre date de naissance au format JJMMAAAA (ex: 30121982)',
    required=True,
)
@click.option(
    '--code', '-c',
    envvar="ING_CODE",
    type=str,
    help='votre mot de passe ING Direct (ex : 123456)',
    prompt='votre mot de passe ING Direct (ex : 123456)',
    hide_input=True,
    required=True,
)
def main():
    pass
if __name__ == '__main__':
    main()