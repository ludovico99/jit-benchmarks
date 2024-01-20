from cProfile import label
from hashlib import new
from tokenize import group
from unittest.mock import patch
import pandas as pd
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from itertools import repeat

GRAPH_TYPE = "C"
# GRAPH_TYPE = "PHP"
# GRAPH_TYPE = "LuaJit"
# GRAPH_TYPE = "Ruby2"

colors = ["#03045e", "#023e8a", "#0077b6", "#0096c7", "#00b4d8", "#48cae4", "#90e0ef"]

#################### only change this #########################

RES_FOLDER = "1705749488_test/"

no_mod_times = pd.read_csv(RES_FOLDER + "no_module.csv")
page_sync_times = pd.read_csv(RES_FOLDER + "page_sync.csv")
zone_sync_times = pd.read_csv(RES_FOLDER + "zone_sync.csv")

times = [0]*3

times[0] = no_mod_times.loc[(no_mod_times["Language"] == GRAPH_TYPE)]
times[1] = page_sync_times.loc[(page_sync_times["Language"] == GRAPH_TYPE)]
times[2] = zone_sync_times.loc[(zone_sync_times["Language"] == GRAPH_TYPE)]
# times[2] = no_mod_times.loc[(no_mod_times["Language"] == GRAPH_TYPE)]

for i in range(len(times)):
    times[i].loc[(times[i]["Test Name"] == "spectralnorm")] = times[i].loc[(times[i]["Test Name"] == "spectralnorm")].replace("spectralnorm", "spectral")
    times[i].loc[(times[i]["Test Name"] == "fannkuchredux")] = times[i].loc[(times[i]["Test Name"] == "fannkuchredux")].replace("fannkuchredux", "fannkuch")

test_names = times[0]["Test Name"].unique()
 
save_name = f"{GRAPH_TYPE}_execution_time.pdf"
graph_title = f"{GRAPH_TYPE} Language"
y_name = "Average Execution Time (s)"
x_name = "Test Name"
labels = ["No LKM", "LKM with page sync check", "LKM with zone sync check"]     
ys = []

for test in test_names:
    for time in times:
        curr_times = time.loc[(time["Test Name"] == test)]
        new_arr = np.array(curr_times["Real Time"])
        ys.append(new_arr)

xs = times[0]["Test Name"].unique()

colors = [colors[0], colors[3], colors[6]]

###############################################################


# err_bar_color = "#d62828"
# err_bar_color = "#778da9"
# err_bar_color = "#b5179e"
# err_bar_color = "#e63946"

group_number = len(labels)
# if (len(ys) < 4):
#     barWidth = 0.25
# else:
#     barWidth = 0.12

barWidth = 0.2
barSpace = 0.05
groupSpace = 5*barSpace
br = [] 
curr = 0.01
for i in range(0, len(ys)):
    if i == 0 or (i+1) % (group_number) != 0:    
        br.append(curr)
        curr += barWidth + barSpace
    else:
        br.append(curr)
        curr += barWidth + groupSpace
        
#br3 = [x + barWidth + barSpace for x in br2]
#br4 = [x + barWidth + barSpace for x in br3]
#br5 = [x + barWidth + barSpace for x in br4]

ticks = []
for i in xs:
    ticks.extend(["", i, ""])

fig, ax = plt.subplots(figsize=(16, 9))
bp = ax.boxplot(ys, positions=br, widths=[barWidth for _ in ys], labels=ticks, showfliers=False)


num_boxes = len(ys)
medians = np.empty(num_boxes)
for i in range(num_boxes):
    box = bp['boxes'][i]
    box_x = []
    box_y = []
    for j in range(5):
        box_x.append(box.get_xdata()[j])
        box_y.append(box.get_ydata()[j])
    box_coords = np.column_stack([box_x, box_y])
    ax.add_patch(Polygon(box_coords, facecolor=colors[i % group_number]))
    
    # median
    med = bp['medians'][i]
    median_x = []
    median_y = []
    for j in range(2):
        median_x.append(med.get_xdata()[j])
        median_y.append(med.get_ydata()[j])
        ax.plot(median_x, median_y, 'k')#, label=labels[i])
    medians[i] = median_y[0]
    
    # mean
    # ax.plot(np.average(med.get_xdata()), np.average(ys[i]),
    #          color='w', markeredgecolor='k')
    
curr_color = 0
for ind, patch in enumerate(bp['boxes']):
    patch.set_color(colors[curr_color])

    curr_color += 1
    curr_color %= group_number 

plt.xlabel(x_name)
plt.ylabel(y_name)
# plt.xticks([r + barWidth + 20*barSpace for r in range(len(ys))], xs)

patches = []
for pos in range(len(labels)):
    patches.append(mpatches.Patch(color=colors[pos], label=labels[pos]))

ax.legend(handles=patches)

# ax.legend(labels)
plt.title(graph_title)

plt.savefig(save_name)

plt.show()
