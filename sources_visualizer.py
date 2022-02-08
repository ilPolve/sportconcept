#!/usr/bin/env python

import os
import json
from collections import defaultdict
from yattag import Doc
from yattag import indent

flows= ['BBC', 'ilPost', 'Televideo', 'Zeit']

BASE_DIR= f"./compared/"

def main():
    date= "2021-11-15"
    sources_a, sources_b, dirs = get_dirs()
    infos= []
    for item in zip(sources_a, sources_b, dirs):
        infos.append(get_infos(item[0], item[1], item[2], date))
    infos= dictionarify(sources_a, infos)
    htmlify(list(set(sources_a)), infos, date)

def get_dirs():
    dirs= []
    sources_a= []
    sources_b= []
    for source_a in os.scandir(BASE_DIR):
        #in teoria servirebbe un else e gestire tutta la questione dei flussi, ma è complicato per via della discrepanza tra confrontare le date e gli epoch
        if not (source_a.name in flows) and source_a.name != "date_comparison":
            dirpath_source_a = f"{BASE_DIR}{source_a.name}/"
            for source_b in os.scandir(dirpath_source_a):
                dirpath_source_b = f"{BASE_DIR}{source_a.name}/{source_b.name}/"
                dirs.append(dirpath_source_b)
                sources_a.append(source_a.name)
                sources_b.append(source_b.name)
    return sources_a, sources_b, dirs

def get_infos(source_a, source_b, my_dir, date):
    for comparison in os.scandir(my_dir):
        this_date = comparison.name.replace(".json", "")
        if this_date == date:
            with open(f"{my_dir}{comparison.name}", "r+") as f:
                this_edition= json.load(f)
            to_ret = {
                'source_a' : source_a,
                'source_b' : source_b,
                'n_sim_titles' : len(this_edition['simils_concepts']),
                'date' : date,
                'dir' : my_dir.replace(BASE_DIR, "../") + comparison.name + ".html"
            }
            return to_ret
    to_ret = {
        'source_a' : source_a,
        'source_b' : source_b,
        'n_sim_titles' : "no_info",
        'date' : date,
        'dir' : ""
    }
    return to_ret

def dictionarify(sources, infos):
    new_infos = defaultdict(list)
    dictionared = False
    for source_a in sources:
        for source_b in sources:
            for info in infos:
                if info['source_a'] == source_a and info['source_b'] == source_b:
                    new_infos[source_a + "-" + source_b] = info
                    new_infos[source_b + "-" + source_a] = info
                    dictionared= True
            if not dictionared:
                new_infos[source_a + "-" + source_b] = None
                new_infos[source_b + "-" + source_a] = None
            dictionared= False
    return new_infos

def htmlify(sources, infos, date):
    to_blank= 0
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    doc.asis('<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">')
    with tag('html'):
        with tag('body'):
            with tag('table', klass= 'table table-bordered'):
                with tag('thead'):
                    with tag('tr', id= "colhead"):
                        with tag('th', id="head"):
                            text(date)
                        for source in sources:
                            with tag('th', id=source + "_col"):
                                text(source)
                    for source_a in sources:
                        with tag('tr'):
                            with tag('th', id=source + "_row"):
                                text(source_a)
                            i= 0
                            to_blank+=1
                            for source_b in sources:
                                current= infos[source_a + "-" + source_b]
                                if i < to_blank:
                                    with tag('td', id=source_a):
                                        text("")
                                else:
                                    if current == None:
                                        with tag('td', klass= "table-dark", id=source_a + "-" + source_b):
                                            text("")
                                    else:
                                        if current['n_sim_titles'] == "no_info":
                                            with tag('td', klass= "table-dark", id=source_a + "-" + source_b):
                                                text("")
                                        elif current['n_sim_titles'] == 0:
                                            with tag('td', klass= "table-danger", id=source_a + "-" + source_b):
                                                with tag('a', href=current['dir']):
                                                    text("0")
                                        elif current['n_sim_titles'] < 3:
                                            with tag('td', klass= "table-warning", id=source_a + "-" + source_b):
                                                with tag('a', href=current['dir']):
                                                    text(current['n_sim_titles'])
                                        else:
                                            with tag('td', klass= "table-success", id=source_a + "-" + source_b):
                                                with tag('a', href=current['dir']):
                                                    text(current['n_sim_titles'])
                                i+=1
    sources_comparison_filepath = f"{BASE_DIR}date_comparison/{date}.html"
    with open(sources_comparison_filepath, "w") as f:
        f.write(indent(doc.getvalue()))
        f.write("\n")

if __name__ == "__main__":
    main()