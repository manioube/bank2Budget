#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import ingdirect as ing

def json2qif(src, tgt): # will convert src json file into tgt qif file
    with open(src) as json_file:
        orig = json.load(json_file)
        # print(orig)
        qif_string = ""
        for op in orig:
            # will set the dates properly, and write them into qif_string
            d_raw = op['effectiveDate']
            # print ("d_raw:", d_raw)
            d = d_raw.split("-")
            inv_d = d[::-1] #this inverts the array
            inv_d_str = '/'.join(inv_d)
            # print ("inv_d_str:", inv_d_str)
            qif_string += "D" + inv_d_str + "\n"

            # will concatenate the amount to the ops
            amount_raw = str('%.2f' % float(op['amount']))
            amount_eur = amount_raw.replace(".", ",") + " €"
            qif_string += "T" + amount_eur + "\n"

            # will concatenate the ops to the dates
            qif_string += "P" + op['detail'] + "\n" + "^" + "\n"

        print ("qif_string:", qif_string)

        # write qif file locally
        f= open(tgt,"w")
        f.write(qif_string)
        f.close()

        return