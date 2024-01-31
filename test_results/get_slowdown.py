from math import nan
import pandas as pd
import numpy as np
import json 
import pdfkit

RES_FOLDER = "1706702098_test/"

no_mod_times = pd.read_csv(RES_FOLDER + "no_module.csv")
page_sync_times = pd.read_csv(RES_FOLDER + "page_sync.csv")
zone_sync_times = pd.read_csv(RES_FOLDER + "zone_sync.csv")

languages = no_mod_times["Language"].unique()
tests = no_mod_times["Test Name"].unique()

medians = {}
slowdown = {
    "Language":[],
    "Test Name":[],
    "LKM Page sync check":[],
    "LKM Zone sync check":[],
}
for l in languages:
    if medians.get(l) == None:
        medians[l] = {}
    for t in tests:
        # no_mod = np.median(np.array())
        # print(no_mod_times.loc[(no_mod_times["Test Name"] == t) & (no_mod_times["Language"] == l), ["Real Time"]])
        no_mod_med = np.median(np.array(no_mod_times.loc[
            (no_mod_times["Test Name"] == t) & (no_mod_times["Language"] == l), 
            ["Real Time"]]))
        page_sync_med = np.median(np.array(page_sync_times.loc[
            (page_sync_times["Test Name"] == t) & (page_sync_times["Language"] == l), 
            ["Real Time"]]))
        zone_sync_med = np.median(np.array(zone_sync_times.loc[
            (zone_sync_times["Test Name"] == t) & (zone_sync_times["Language"] == l), 
            ["Real Time"]]))

        medians[l][t] = (no_mod_med, page_sync_med, zone_sync_med)

        if no_mod_med != nan:
            slowdown["Language"].append(l)
            slowdown["Test Name"].append(t)
            slowdown["LKM Page sync check"].append((page_sync_med-no_mod_med)/no_mod_med)
            slowdown["LKM Zone sync check"].append((zone_sync_med-no_mod_med)/no_mod_med)
        
        print(f"LANGUAGE: {l}, TEST: {t} --> PAGE_SYNC: ${(page_sync_med-no_mod_med)/no_mod_med*100:.2f}% - ZONE_SYNC: ${(zone_sync_med-no_mod_med)/no_mod_med*100:.2f}%")

# print(json.dumps(medians, indent=1))

slow_pd = pd.DataFrame(slowdown)

print(slow_pd)

slow_pd.to_csv("slowdown.csv")
