import json
import os
import matplotlib.pyplot as plt

FONTSIZE = 20
plt.rc('font', weight='bold')

SEP = "\\"
# SEP = "/"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = f"{BASE_DIR}{SEP}out{SEP}triple_def_out"

MONTH = 3
DAYS = range(11, 16)
TOT_DAYS = len(list(DAYS))

OUTLETS = [f"DE{SEP}Spiegel", f"IT{SEP}ilPost", f"IT{SEP}ANSA_Esteri", f"FR{SEP}France24", f"ES{SEP}ABC", f"EN{SEP}BBC"]


def single_language(outlet: str, ratio: bool = False):
    excl, skip, com = get_values(outlet, ratio)
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    ax = plt.subplot(111)
    w = 0.3
    bars = []
    for i, day in zip(range(TOT_DAYS), DAYS):
        rect = ax.bar(i - w, excl[i], width=w, align='center', color=colors[0])
        autolabel(rect, ax)
        rect = ax.bar(i, skip[i], width=w, align='center', color=colors[1])
        autolabel(rect, ax)
        rect = ax.bar(i + w, com[i], width=w, align='center', color=colors[2])
        autolabel(rect, ax)
    rect = ax.bar(TOT_DAYS - w, excl[TOT_DAYS], width=w, align='center', color=colors[0])
    autolabel(rect, ax)
    bars.append(rect)
    rect = ax.bar(TOT_DAYS, skip[TOT_DAYS], width=w, align='center', color=colors[1])
    autolabel(rect, ax)
    bars.append(rect)
    rect = ax.bar(TOT_DAYS + w, com[TOT_DAYS], width=w, align='center', color=colors[2])
    autolabel(rect, ax)
    bars.append(rect)
    ax.legend(bars, ["Exclusive", "Skipped", "Common"], fontsize = FONTSIZE-7)
    x_ticks = [f"{day}-{day+12}" for day in DAYS] + ["Total"]
    plt.xticks(range(TOT_DAYS + 1), x_ticks)
    ratio_str = " divided by total" if ratio else ""
    plt.title(f"SCE from {outlet}{ratio_str} in {TOT_DAYS} days", fontsize=FONTSIZE, weight = "bold")
    plt.xlabel("Timespan", fontsize=FONTSIZE, weight = "bold")
    plt.ylabel("Number of news", fontsize=FONTSIZE, weight = "bold")
    plt.show()


def get_values(outlet, ratio):
    excl = []
    skip = []
    com = []
    for i in DAYS:
        with open(f"{JSON_DIR}_{i}_{MONTH}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            excl.append(data[outlet]["exclusive"])
            skip.append(data[outlet]["skipped"])
            com.append(data[outlet]["common"])
    with open(f"{JSON_DIR}_{TOT_DAYS}days.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        excl.append(data[outlet]["exclusive"])
        skip.append(data[outlet]["skipped"])
        com.append(data[outlet]["common"])
    if ratio:
        for i in range(len(excl)):
            total = excl[i] + skip[i] + com[i]
            excl[i] = excl[i] / total
            skip[i] = skip[i] / total
            com[i] = com[i] / total
    return excl, skip, com


def columned_bars(ratio: bool = False):
    mean_vals = []
    tot_vals = []
    for outlet in OUTLETS:
        excl, skip, com = get_values(outlet, ratio)
        excl_mean = sum(excl[:-1]) / len(excl[:-1])
        skip_mean = sum(skip[:-1]) / len(skip[:-1])
        com_mean = sum(com[:-1]) / len(com[:-1])
        mean_vals.append((excl_mean, skip_mean, com_mean))
        tot_vals.append((excl[-1], skip[-1], com[-1]))
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    ax = plt.subplot(111)
    w = 0.3
    for i in range(len(OUTLETS)):
        rect1 = ax.bar(i - (w / 2), mean_vals[i][0], width=w, align='center', color=colors[0])
        autolabel(rect1, ax)
        rect2 = ax.bar(i - (w / 2), mean_vals[i][1], width=w, align='center', color=colors[1],
                       bottom=mean_vals[i][0])
        autolabel(rect2, ax, true_h=rect2[0].get_height() + mean_vals[i][0])
        rect3 = ax.bar(i - (w / 2), mean_vals[i][2], width=w, align='center', color=colors[2],
                       bottom=mean_vals[i][0] + mean_vals[i][1])
        autolabel(rect3, ax, true_h=rect3[0].get_height() + mean_vals[i][0] + mean_vals[i][1])

        rect1_tot = ax.bar(i + (w / 2), tot_vals[i][0], width=w, align='center', color=colors[0], edgecolor='black',
                           hatch='.')
        autolabel(rect1_tot, ax)
        rect2_tot = ax.bar(i + (w / 2), tot_vals[i][1], width=w, align='center', color=colors[1],
                           bottom=tot_vals[i][0], edgecolor='black', hatch='.')
        autolabel(rect2_tot, ax, true_h=rect2_tot[0].get_height() + tot_vals[i][0])
        rect3_tot = ax.bar(i + (w / 2), tot_vals[i][2], width=w, align='center', color=colors[2],
                           bottom=tot_vals[i][0] + tot_vals[i][1], edgecolor='black', hatch='.')
        autolabel(rect3_tot, ax, true_h=rect3_tot[0].get_height() + tot_vals[i][0] + tot_vals[i][1])
        if i == len(OUTLETS) - 1:
            ax.legend([rect1, rect2, rect3], ["Exclusive", "Skipped", "Common"], fontsize=FONTSIZE-7)
    x_ticks = [outlet.split(f"{SEP}")[1] for outlet in OUTLETS]
    plt.xticks(range(len(OUTLETS)), x_ticks)
    plt.title(f"SCE averages from {TOT_DAYS} days compared to {TOT_DAYS} days snapshot", fontsize=FONTSIZE, weight = "bold")
    plt.xlabel("Outlet", fontsize=FONTSIZE, weight = "bold")
    plt.ylabel("Number of news", fontsize=FONTSIZE, weight = "bold")
    plt.show()


def autolabel(rects, ax, true_h=-1):
    for rect in rects:
        h = rect.get_height()
        if true_h != -1:
            h = true_h
        if rect.get_height() <= 0:
            return
        ax.text(rect.get_x() + rect.get_width() / 2., h, f"{rect.get_height():.2f}",
                ha='center', va='bottom', fontsize=FONTSIZE-6, weight="bold")


def main():
    # for outlet in OUTLETS:
    #     single_language(outlet, True)
    columned_bars(True)


if __name__ == "__main__":
    main()
