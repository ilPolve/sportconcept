import json
import numpy as np
import matplotlib.pyplot as plt

hours = 24

def main():
    triple_def_visual()

def triple_def_visual():
    triple_def_data = {}
    color = [1, 25, 50, 100, 150, 200, 300, 450, 550, 600, 650]
    with open(f"triple_def_out_{hours}.json") as fp:
        triple_def_data = json.load(fp)
    names = []
    x_skip = []
    y_com = []
    z_excl = []
    for source in triple_def_data:
        # names.append(source.split("/")[1])
        names.append(source.split("\\")[1])
        x_skip.append(triple_def_data[source]["skipped"])
        y_com.append(triple_def_data[source]["common"])
        z_excl.append(triple_def_data[source]["exclusive"])
    title = "S.C.E. news considering "
    hours_title = "1 snapshot" if hours == 1 else f"{hours} hours"
    plt.scatter(x_skip, y_com, s=[100*(z+1) for z in z_excl], c = color[:len(x_skip)])
    for i, txt in enumerate(names):
        plt.annotate(f"{txt}  [{z_excl[i]}]", ((z_excl[i])/100 + (x_skip[i]+1), (z_excl[i]+1)/100 + (y_com[i])))
    plt.xlabel("Skipped news")
    plt.ylabel("Covered news")
    plt.title(f"{title}{hours_title}")
    plt.show()
    return

if __name__ == '__main__':
    main()