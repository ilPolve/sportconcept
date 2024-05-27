#!/usr/bin/env python

import json
import os
import sys
import errno

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

BASE_URL = f"full_compared/"

START_HOUR = "16"

DATE = "2022-05-12"

TO_DO = ["ANSA_CrEsPo/AGI_CrEsPo", 
         "ANSA_CrPo/AGI_CrPo", 
         "ANSA_EsPo/AGI_EsPo", 
         "ANSA_Cronaca/AGI_Cronaca", 
         "ANSA_Esteri/AGI_Esteri", 
         "ANSA_Politica/AGI_Politica"]

LONG_TO_AB = {"ANSA": "A", "AGI": "B"}

DIR_TO_TITLE = {"ANSA_CrEsPo/AGI_CrEsPo": "CronacaEsteriPolitica",
                "ANSA_CrPo/AGI_CrPo": "CronacaPolitica",
                "ANSA_EsPo/AGI_EsPo": "EsteriPolitica",
                "ANSA_Cronaca/AGI_Cronaca": "Cronaca",
                "ANSA_Esteri/AGI_Esteri": "Esteri",
                "ANSA_Politica/AGI_Politica": "Politica"}

SLICES_RANGE = range(1, 8)

def main():
    plt.close()

    for dir in TO_DO:
        two_visualizer(f"{BASE_URL}{dir}/{DATE}", "AGI", "ANSA", DIR_TO_TITLE[dir])
        two_visualizer(f"{BASE_URL}{dir}/{DATE}", "ANSA", "AGI", DIR_TO_TITLE[dir])

def two_visualizer(path, longer, analyzed, pre_title):
    excl_st = []
    excl_cos = []

    len_a = []
    len_b = 0

    slices= [f"{START_HOUR}+-{str(slice)}" for slice in SLICES_RANGE]

    pathnames_st = get_pathnames(path, "", longer)
    pathnames_cos = get_pathnames(path, "cos_", longer)

    for pathnames in zip(pathnames_st, pathnames_cos):
        curr_comp_st = file_open(pathnames[0])
        curr_comp_cos = file_open(pathnames[1])

        excl_st.append(get_exclusivity(curr_comp_st, analyzed))
        excl_cos.append(get_exclusivity(curr_comp_cos, analyzed))

        changed, len_b = get_length(curr_comp_st, longer, analyzed)

        len_a.append(changed)


    df = pd.DataFrame(np.array([excl_st, excl_cos]).transpose(), index= range(0, 7), columns= [f"Standard Algorithm", f"Cosine Algorithm"])

    cell_text= []
    for row in range(len(df)):
        cell_text.append(df.iloc[row])

    table = plt.table(cellText=cell_text, colLabels=df.columns, rowLabels=slices, loc='center')
    plt.axis('off')
    table.set_fontsize(14)
    table.scale(1, 3)

    fig = plt.figure(constrained_layout=True)

    gs= GridSpec(2,2, figure=fig)


    fig.suptitle(f"\n{pre_title} cluster: {longer} grower, {analyzed} pivot\n", fontsize=16)
    fig.tight_layout()
    ax1= fig.add_subplot(gs[0:, 0])
    ax2= fig.add_subplot(gs[0, 1])
    ax3= fig.add_subplot(gs[1, 1])

    plt1 = df.plot(title=f"{analyzed} exclusivity percentage\n", ax=ax1, style='o-')
    ax1.set_xticks(df.index, slices)
    table2 = ax2.table(cellText= np.array([len_a]).transpose(), colLabels=[f"Changing number of {longer} news"], rowLabels=slices, colWidths=[0.9], loc='center')
    ax2.axis('off')
    table2.auto_set_font_size(False)
    table2.set_fontsize(12)
    table2.auto_set_column_width(col=list(range(1)))
    table2.scale(1, 2)
    ax3.text(0.4, 0.8, f"Number of {analyzed} news: {len_b}", va="center", ha="center", size=14)
    ax3.axis('off')
    plt.show()

def get_pathnames(base, prefix, longer):
    to_ret = []
    for i in SLICES_RANGE:
        to_ret.append(f"{base}/{prefix}{START_HOUR}+-{i}_{longer}.json")
    return to_ret

def file_open(path):
    with open(path, "r") as f:
        try:
            curr_comp = json.load(f)
        except:
            raise Exception("Could not read file from the given directory: " + path + ".")
    return curr_comp

def get_exclusivity(comp, analyzed):
    return comp[f"exclusivity_{LONG_TO_AB[analyzed]}_percent"]

def get_length(comp, longer, analyzed):
    return comp[f"len_{LONG_TO_AB[longer]}"], comp[f"len_{LONG_TO_AB[analyzed]}"]

if __name__ == '__main__':
    main()
