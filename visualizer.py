import os
import json
from collections import defaultdict
from yattag import Doc
from yattag import indent

editions_name= ["CH/RTS/", "DE/Tagesschau/", "DE/Zdf/",
                "FR/France24/", "IT/GR1/", "US/PBS/"]

flows_name= [ "DE/Zeit/", "IT/ilPost/", "IT/Televideo/", "UK/BBC/", "US/NYT/"]

editions_name = ["CH/RTS/", "DE/Tagesschau", "FR/France24"]

#a function that deletes from filenames utility strings
def string_format(to_format):
    return to_format.replace("conc_", "").replace("en_", "")

def simil_format(to_format):
    filename_a = to_format["news"][0]["source"] + "/" + string_format(to_format["news"][0]["filename"])
    filename_b = to_format["news"][1]["source"] + "/" + string_format(to_format["news"][1]["filename"])
    return filename_a + "-" + filename_b

def simil_format_title(to_format):
    title_a = to_format['news'][0]['en_title']
    title_b = to_format['news'][1]['en_title']
    return title_a + "--" + title_b

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

def get_news(to_get):
    titles = []
    for subdir in to_get:
        directory = "../newScraping/collectedNews/" + subdir
        for jfile in os.scandir(directory):
            f= open(directory + "/" + jfile.name, "r+")
            curr_news= json.load(f)
            f.close()
            for new in curr_news:
                if jfile.name[0] == 'e' or jfile.name[0] == 'c':
                    titles.append(new['en_title'] + "___in edition___" + new['source'] + "/" + string_format(new['filename']))
    return titles


#a function which generate che list of simil editions 
def get_simm_list(directory):
    news_names = defaultdict(list)
    simm_list = []
    f= open(directory, "r+")
    json_file = json.load(f)
    f.close()
    for simils in json_file:
        simm_list.append(simil_format(simils))
        news_names[simil_format(simils)].append(simils["news"][0]["en_title"] + "_____is simil to_____" + simils["news"][1]["en_title"])
    return simm_list, news_names


def get_simils_by_title(filename):
    concept_names = defaultdict(list)
    simm_list= []
    f= open(filename, "r+")
    json_file= json.load(f)
    f.close()
    for simils in json_file:
        simm_list.append(simil_format_title(simils))
        for to_app in simils['concepts']['concepts_found']:
            concept_names[simil_format_title(simils)].append(to_app['word'])
    return simm_list, concept_names

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
                                        to_print+= titles + "-----------------"
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

def get_simm_table_title(to_tab, simils, simil_concepts, is_edit):
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
                        for title in to_tab:
                            with tag('th', ('scope', 'row'), id="col_"+title):
                                text(title)
                for title in to_tab:
                    with tag('tr', id="rowhead"):
                        with tag('th', ('scope', 'row'), id="row_"+title):
                            text(title)
                        for title_b in to_tab:
                            if title + "--" + title_b in simils:
                                with tag('th', klass= 'table-success', id= title + "--" + title_b):
                                    to_print= ""
                                    for concepts in simil_concepts[title+"--"+title_b]:
                                        to_print+=concepts + "--------------"
                                    text(to_print)
                            else:
                                with tag('th', klass= 'table-danger', id=title + "--" + title_b):
                                    text("")
    if is_edit:
        f= open("editions_title.html", "w")
    else:
        f= open("flows_title.html", "w")
    f.write(indent(doc.getvalue()))
    f.close()

            
def main():
    editions = get_editions(editions_name)
    flows = get_editions(flows_name)
    editions_title = get_news(editions_name)
    #flows_title = get_news(flows_name)

    #editions_simils, edit_names = get_simm_list("editions_simils.txt")
    #flows_simils, flow_names = get_simm_list("flows_simils.txt")
    editions_simils_title, edit_names_title = get_simils_by_title("editions_simils.txt")
    #flows_simils_title, flow_names_title = get_simils_by_title("flows_simils.txt")

    #get_simm_table(editions, editions_simils, edit_names, True)
    #get_simm_table(flows, flows_simils, flow_names, False)
    get_simm_table_title(editions_title, editions_simils_title, edit_names_title, True)
    #get_simm_table_title(flows_title, flows_simils_title, flow_names_title, False)

    #print(editions)
    #print(flows)

if __name__ == "__main__":
    main()