import json
import matplotlib.pyplot as plt
import numpy as np
import os

DIGITS = 3

def main():
    sce_visual()

def sce_visual():
    sce_data = {}
    for file in os.listdir("./"):
        if file.endswith(".json") and "ANSA" not in file and "triple" in file:
            print(file.split("."))
            idx = file.split(".")[-2].split("_")[-1]
            with open(file) as fp:
                sce_data[int(idx)] = json.load(fp)

    sorted_data = sorted(sce_data)
    skipped = {"FR\\France24": []}
    common =  {"FR\\France24": []}
    exclusive =  {"FR\\France24": []}
    for key in skipped:
        for idx in sorted_data:
            total_news = sce_data[idx][key]["skipped"] + sce_data[idx][key]["common"] + sce_data[idx][key]["exclusive"]
            skipped[key].append(round(sce_data[idx][key]["skipped"] / total_news, DIGITS))
            common[key].append(round(sce_data[idx][key]["common"] / total_news, DIGITS))
            exclusive[key].append(round(sce_data[idx][key]["exclusive"] / total_news, DIGITS))

    for key in skipped:
        plt.plot(sorted_data, skipped[key], "-o", label="Skipped")
        plt.plot(sorted_data, common[key], "-o", label="Common")
        plt.plot(sorted_data, exclusive[key], "-o", label="Exclusive")
        plt.title(f"Rate of S.C.E. news of {key}")
        plt.xlabel("Considered hours")
        plt.ylabel("News rate")
        plt.legend()
        plt.show()

        plt.plot(sorted_data, skipped[key], "-o", label="Skipped")
        plt.title(f"Skipped news of {key}")
        plt.xlabel("Considered hours")
        plt.ylabel("News rate")
        plt.show()

        plt.plot(sorted_data, common[key], "-o", label="Common")
        plt.title(f"Common news of {key}")
        plt.xlabel("Considered hours")
        plt.ylabel("News rate")
        plt.show()

        plt.plot(sorted_data, exclusive[key], "-o", label="Exclusive")
        plt.title(f"Exclusive news of {key}")
        plt.xlabel("Considered hours")
        plt.ylabel("News rate")
        plt.show()
        #sce of france24
    
if __name__ == "__main__":
    main()