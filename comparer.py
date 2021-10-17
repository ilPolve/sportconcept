import json
import os

nations= ['CH', 'DE', 'FR', 'IT', 'UK', 'US']

ed_type= ["RTS", "Tagesschau", "Zdf", "France24", "GR1", "PBS"]
flow_type= ["Zeit", "Televideo", "ilPost", "BBC", "NYT"]

editions_by_source= {'RTS': [], 'Tagesschau': [], 'Zdf': [], 'France24': [], 'GR1': [], 'PBS': []}
flows_by_source= {'Zeit': [], 'Televideo': [], 'ilPost': [], 'BBC': [], 'NYT': []}

def jsonizer(directory):
    f= open(directory, "r+")
    print(directory)
    to_ret= json.load(f)
    f.close()
    return to_ret

def news_getter(nation, source):
    directory= "../newScraping/collectedNews/" + nation + "/" + source
    print(source)
    if source in ed_type:
        for to_append in os.scandir(directory):
            editions_by_source[source].append(jsonizer(directory + "/" + to_append.name))
    elif source in flow_type:
            for to_append in os.scandir(directory):
                flows_by_source[source].append(jsonizer(directory + "/" + to_append.name))
    else:
        print("Source not recognized")
            

for nation in nations:
    dir= "../newScraping/collectedNews/" + nation
    for source_dir in os.scandir(dir):
        source= source_dir.name
        news_getter(nation, source)
