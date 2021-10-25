import os
import json
from collections import defaultdict
from yattag import Doc
from yattag import indent

editions_name= ["CH/RTS/", "DE/Tagesschau/", "DE/Zdf/",
                "FR/France24/", "IT/GR1/", "US/PBS/"]

flows_name= [ "DE/Zeit/", "IT/ilPost/", "IT/Televideo/", "UK/BBC/", "US/NYT/"]

#a function that deletes from filenames utility strings
def string_format(to_format):
    return to_format.replace("conc_", "").replace("en_", "")

def simil_format(to_format):
    filename_a = to_format["news"][0]["source"] + "/" + string_format(to_format["news"][0]["filename"])
    filename_b = to_format["news"][1]["source"] + "/" + string_format(to_format["news"][1]["filename"])
    return filename_a + "-" + filename_b
#a function that, given a subdirectory, list its edition files
def get_editions(to_get):
    to_ret= []
    directory= "../newScraping/collectedNews/"
    for subdir in to_get:
        curr_dir= directory + subdir
        for found in os.scandir(curr_dir):
            source = curr_dir.split("/")
            source = source[len(source)-2]
            to_ret.append(string_format(source + "/" + found.name))
    return to_ret

#a function which generate che list of simil editions 
def get_simm_list(directory):
    news_names = defaultdict(list)
    simm_list = []
    f= open(directory, "r+")
    json_file = json.load(f)
    f.close()
    for simils in json_file:
        simm_list.append(simil_format(simils))
        news_names[simil_format(simils)].append(simils["news"][0]["title"] + "_____is simil to_____" + simils["news"][1]["title"])
    return simm_list, news_names

#a yattag function which creates the similarity table
def get_simm_table(to_tab, simils, simil_names, is_edit):
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    doc.asis('<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">')
    with tag('html'):
        with tag('body'):
            with tag('table', klass= 'table table-bordered'):
                with tag('thead'):
                    with tag('tr', id= "colhead"):
                        with tag('th', id="head"):
                            text("")
                        for edition in to_tab:
                            with tag('th', ('scope', 'col'), id="col_"+edition):
                                text(edition)
                for edition in to_tab:
                    with tag('tr', id="rowhead"):
                        with tag('th', ('scope', 'row'), id="row_"+edition):
                            text(edition)
                        for edition_b in to_tab:
                            if edition + "-" + edition_b in simils:
                                with tag('th', klass = 'table-success', id=edition + "-" + edition_b):
                                    to_print= ""
                                    for titles in simil_names[edition+"-"+edition_b]:
                                        to_print+= titles + "\n"
                                    text(to_print)
                            else:
                                with tag('th', klass = 'table-danger', id=edition + "-" + edition_b):
                                    text("")
                            
    if is_edit:
        f=open("editions.html", "w")
    else:
        f=open("flows.html", "w")
    f.write(indent(doc.getvalue()))
    f.close()
    #print(indent(doc.getvalue()))
            

editions = get_editions(editions_name)
flows = get_editions(flows_name)

editions_simils, edit_names = get_simm_list("editions_simils.txt")
flows_simils, flow_names = get_simm_list("flows_simils.txt")
get_simm_table(editions, editions_simils, edit_names, True)
get_simm_table(flows, flows_simils, flow_names, False)


#print(editions)
#print(flows)