
"""
This program takes a text file(s) converted from pdf of a webpage with tables created by WIPO
and output a csv file.

Usage: python3 ipdconverter.py
run in the same directory as the *txt files
by Aye Wollam
"""

import csv
import os
import sys
# returns a list
import glob

text_files = glob.glob("*.txt")
headers = ["e-fiing reference",	"date","status","trademark","summary"]


def trademark(status, line_list):
    tradem = line_list[0].split(status)[-1].strip()
    if len(tradem) == 0:
        tradem = "LOGO"
    return tradem


for file in text_files:
    with open(file,"r") as f, open("outfile.csv","w") as o:
        o_writer = csv.DictWriter(o, fieldnames=headers)
        o_writer.writeheader()
        for l in f:
            results_dict = dict.fromkeys(headers, "NA")
            l = l.strip()
            # print(len(l))
            if len(l) == 0:
                continue
            if "WFT" in l:
                standard_split = l.split()
                results_dict["e-fiing reference"] = standard_split[0]
                # split by the word Nice
                nice_split = l.split('Nice Classification Nbr:')

                results_dict["summary"] = f"Nice Classification Nbr {nice_split[-1]}"
                if "Received" in l:
                    results_dict["trademark"] = trademark("Received", nice_split)
                    results_dict["date"] = standard_split[1]
                    results_dict["status"] = "Received"

                if "Draft" in l:

                    results_dict["trademark"] = trademark("Draft", nice_split)

                    results_dict["status"] = "Draft"
                 # print(results_dict)

                if "Pending" in l:

                    results_dict["trademark"] = trademark("Pending Submission Confirmation", nice_split)

                    results_dict["status"] = "Pending Submission Confirmation"
                    # print(results_dict)
                o_writer.writerow(results_dict)



