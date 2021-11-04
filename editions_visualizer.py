import os
import json
from collections import defaultdict
from yattag import Doc
from yattag import indent

def main():
    my_files = get_dirs()
    for my_file in my_files:
        htmlify(my_file)

#a util function which, in my filesystem, gets the path of all comparison files
def get_dirs():
    to_ret= []
    directory= "./compared/"
    for source_a in os.scandir(directory):
        subdir_a = directory + source_a.name + "/"
        for source_b in os.scandir(subdir_a):
            subdir_b = subdir_a + source_b.name + "/"
            for my_compare in os.scandir(subdir_b):
                to_ret.append(subdir_b + my_compare.name)
    return to_ret

#a function which, given the path of a json comparing file, visualize its html table of comparison
def htmlify(path):
    f= open(path, "r+")
    compared = json.load(f)
    f.close()
    to_visual_name = path.split("/")
    to_visual_name = to_visual_name[len(to_visual_name)-1]
    simils, simil_concs = get_simils(compared)
    print_table(compared, to_visual_name, simils, simil_concs)

def get_simils(compared):
    compared= compared['simils_concepts']
    simm_list= []
    simm_table= defaultdict(list)
    for similar in compared:
        simm_name= similar['news'][0]['en_title'] + "----" + similar['news'][1]['en_title']
        simm_list.append(simm_name)
        for concept in similar['concepts']['concepts_found']:
            simm_table[simm_name].append(concept['word'])
    return simm_list, simm_table

def print_table(to_visual, to_visual_name, simils, simil_table):
    header_a = []
    header_b = []
    for new in to_visual['edition_a']:
        header_a.append(new['en_title'])
    for new in to_visual['edition_b']:
        header_b.append(new['en_title'])

if __name__ == "__main__":
    main()