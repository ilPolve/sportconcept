import matplotlib.pyplot as plt
import numpy as np
import json
import sys

def main(file):
    with open(f'../out/{file}', 'r') as fd:
        data = json.load(fd)
        
        labels = set()
        sources = data.keys()
        for source in sources:
            for date in data[source].keys():
                for label in data[source][date].keys():
                    labels.add(label)
        
        dates = sorted(list(data[list(data.keys())[0]].keys()))
        labels.remove('daily_news_count')

        for date in dates:
            total_values = dict()
            for source in sources:
                total_values[source] = dict()
            
            for i, label in enumerate(labels):
                for source in sources:
                    try:
                        total_values[source][label] = len(data[source][date][label])
                    except:
                        total_values[source][label] = 0
            
            print(list(sorted(labels)))
            labels = filter(lambda l: sum([total_values[source][l] for source in sources]) > 0, labels)
            sorted_labels = sorted(labels, key=lambda l: sum([total_values[source][l] for source in sources]))
            try:
                sorted_labels.remove('non classificabile')
                sorted_labels.remove('notizie non sportive')
                sorted_labels = ['non classificabile', 'notizie non sportive', *sorted_labels]
            except:
                print('Except')
            
            x = np.arange(len(sorted_labels))
            width = 0.2
            fig, ax = plt.subplots(figsize=(16, 8))
            
            bar_colors = ["#fde9eb","#f50f3b", "#9e4931"]                
            for i, source in enumerate(sources):
                pos = -1 if i < 1 else 1 if i > 1 else 0
                ax.bar(x + pos * width * 1.25, [total_values[source][label] for label in sorted_labels], width * 1.25, label=source.upper(), edgecolor='black', color=bar_colors[i])
            
            ax.set_ylabel('# of article')
            ax.set_title(f'Dati del {date}')

            ax.set_xticks(x)
            ax.set_xticklabels(sorted_labels, rotation=45, ha='right')
            # Sposta la legenda in alto a sinistra
            ax.legend(loc="upper left")

            fig.tight_layout()
            plt.show()
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Too few arguments.")
    else:
        main(sys.argv[1])

