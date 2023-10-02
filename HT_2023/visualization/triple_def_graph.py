import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

plt.rc('font', weight='bold')
plt.rc('axes', axisbelow = True)

FONTSIZE =24
HOURS = [1]

JSON_DIR = f"special_issue\\triple_def_out_prova.json"

def main():
    for hour in HOURS:
        triple_def_visual(hour)

def triple_def_visual(hours):
    triple_def_data = {}
    with open(JSON_DIR) as fp:
        triple_def_data = json.load(fp)
    names = []
    x_skip = []
    y_com = []
    z_excl = []
    for source in triple_def_data:
        if source != "IT\\ANSA_Esteri":
        # names.append(source.split("/")[1])
            names.append(source.split("\\")[1])
            x_skip.append(triple_def_data[source]["skipped"])
            y_com.append(triple_def_data[source]["common"])
            z_excl.append(triple_def_data[source]["exclusive"])
    names.append("ANSA_Esteri")
    x_skip.append(triple_def_data["IT\\ANSA_Esteri"]["skipped"])
    y_com.append(triple_def_data["IT\\ANSA_Esteri"]["common"])
    z_excl.append(triple_def_data["IT\\ANSA_Esteri"]["exclusive"])
    tot_news = triple_def_data["DE\\Spiegel"]["skipped"] + triple_def_data["DE\\Spiegel"]["common"] + triple_def_data["DE\\Spiegel"]["exclusive"]
    if "ANSA_Esteri" in names:
        x_c = np.arange(len(x_skip)-1)
        y_c = [i+x_c+(i*x_c)**2 for i in range(len(x_skip)-1)]
        colors = cm.rainbow(np.linspace(0, 1, len(y_c)))
    x_c = np.arange(len(x_skip)+1)
    y_c = [i+x_c+(i*x_c)**2 for i in range(len(x_skip)+1)]
    ansa_color = cm.rainbow(np.linspace(0,1, len(y_c)))

    title = "S.C.E. news considering "
    hours_title = "1 snapshot" if hours == 1 else f"{hours} hours"

    print(tot_news)

    # plot the diagonal line along all the graph
    plt.plot([tot_news, 0], [0, tot_news], color="black", linestyle="--", linewidth=2)

    plt.grid()
    for i in range(len(x_skip)-1):
        print(colors[i])
        print(names[i])
        print(i)
        plt.scatter(x_skip[i], y_com[i], s=[400*(z_excl[i]+7)], color = colors[i], label=f"{names[i]} [{z_excl[i]}]")
    plt.scatter(x_skip[len(x_skip)-1], y_com[len(y_com) - 1], s=[400*(z_excl[len(z_excl)-1] + 7)], color = [0.8, 0.1, 0.7, 1], label=f"{names[len(names)-1]} [{z_excl[len(z_excl)-1]}]")
    # for i, txt in enumerate(names):
    #     plt.annotate(f"[{z_excl[i]}]", ((z_excl[i]+5)/35 + (x_skip[i]+3), (z_excl[i]+5)/35 + (y_com[i]+3)), fontsize = FONTSIZE)
    plt.xticks(fontsize=FONTSIZE-3)
    plt.yticks(fontsize=FONTSIZE-3)
    plt.xlabel("Skipped news", fontsize=FONTSIZE, weight="bold")
    plt.ylabel("Covered news", fontsize=FONTSIZE, weight="bold")
    plt.title(f"{title}{hours_title}", fontsize=FONTSIZE, weight="bold")
    lgnd = plt.legend(fontsize=FONTSIZE-4)
    for i in range(len(x_skip)):
        lgnd.legendHandles[i]._sizes = [80]
    plt.show()
    return

if __name__ == '__main__':
    main()