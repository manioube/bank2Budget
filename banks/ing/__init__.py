# -*- coding: utf-8 -*-

from .client import Client
import settings

import random
from datetime import datetime


__version__ = '0.1.2'  # En cohérence avec setup.py
# Permet à Sphinx de récupérer ces éléments pour la documentation
__all__ = ['Client']


def main(
        num_client = settings.ING['ACCOUNT'],
        date_naissance = settings.ING['DOB'],
        code = settings.ING['CODE']
):
    ing = Client()
    ing._login(num_client=num_client, date_naissance=date_naissance)
    ing._recuperer_url_keypad()
    ing._recuperer_keypad()
    ing._code_a_saisir(code_complet=code)
    ing._recuperer_coord_chiffres()
    ing._saisie_code()
    ing._infos_client()
    retour_synthese_comptes = ing._synthese_comptes()
    retour_ops = ing._get_ops()
    ing._logout()
    now = datetime.now()
    current_time = now.strftime("%d-%m-%y @ %H:%M:%S")
    data = {
        "bank" : "ing",
        "retour_synthese_comptes": retour_synthese_comptes,
        "retour_ops": retour_ops,
        "message": "data was retrieved from ING"
    }
    return data

