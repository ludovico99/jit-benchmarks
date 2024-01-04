from re import S
import subprocess
import sys
import numpy as np
import os, shutil
import locale
import pandas as pd

def run_command(cmd):
    cmd_out = subprocess.run(cmd,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True,
        shell=True,
        executable="/bin/bash")

    return cmd_out

def run_time_command(cmd, executions):
    full_command = f'time -p for i in $(seq 0 {executions}); do {cmd}; done;'
    timed_perf = run_command(full_command)

    lines = timed_perf.stderr.split("\n")
    
    real_time = lines[-4].split(" ")[1]
    user_time = lines[-3].split(" ")[1]
    sys_time = lines[-2].split(" ")[1]
    
    real_time = float(real_time.replace(",", "."))
    user_time = float(user_time.replace(",", "."))
    sys_time = float(sys_time.replace(",", "."))

    return (real_time, user_time, sys_time)

class Language:
    def __init__(self, name, extension, run_cmd, jit, needs_build=False,build_cmd=None, out_build=None):
        self.name = name
        self.extension = extension
        self.run_cmd = run_cmd
        self.jit = jit
        self.needs_build = needs_build
        self.build_cmd = build_cmd
        self.out_build = out_build
    
    def __repr__(self):
        return f"Language({self.name}, JIT={self.jit})"

    def build(self, file):
        if self.needs_build:
            return run_command(self.build_cmd.format(file))
    
    def run(self, file):
        if self.needs_build:
            self.build(file)
            out = run_command(self.run_cmd.format(self.out_build))
            run_command(f"rm {self.out_build}")
            return out
        else:    
            return run_command(self.run_cmd.format(file))

    def time_run(self, file, executions):
        if self.needs_build:
            self.build(file)
            out = run_time_command(self.run_cmd.format(self.out_build), executions)
            run_command(f"rm {self.out_build}")
            return out
        else:    
            return run_time_command(self.run_cmd.format(file), executions)

TESTED_LANGUAGES = [
    Language("C", ".c", "./{}", False, True, "gcc {} -o a.out -lm", "a.out"),
    #https://stitcher.io/blog/php-8-jit-setup
    Language("PHP", ".php", "php -dopcache.enable_cli=1 -dopcache.enable=1 -dopcache.jit_buffer_size=500M -dopcache.jit=1255 {}", True, False),
    Language("LuaJit", ".lua", "luajit {}", True, False),
    Language("Ruby2", ".rb", "ruby --jit {}", True, False) # No WX pages????
]

SRC_FOLDER = "."

TEST_NUMBER = 10

EXECUTIONS = {
    "fasta":1,
    "matmul":1,
    "brainfuck":1,
    "fannkuchredux":1,
    #"spectralnorm":1,
    "knucleotide":1,
    "nbody":1,
    "binarytrees":1,
}

time_info = {
        "Language": [],
        "Test Name": [],
        "Real Mean Time": [],
        "User Mean Time": [],
        "Sys Mean Time": [],
        "Real Var Time": [],
        "User Var Time": [],
        "Sys Var Time": [],
        "Executions": [],
        "Test Size": [],
    }
print(f"Getting files from: {SRC_FOLDER}")
for root, subdirs, files in os.walk(SRC_FOLDER):

    for filename in files:
        file_path = os.path.join(root, filename)

        _, file_extension = os.path.splitext(file_path)
        
        for l in TESTED_LANGUAGES:
            if "spectralnorm" in file_path:
                continue

            # this are too slow or dont work
            if l.name == "PHP" and "knucleotide" in file_path:
                continue

            if l.name == "LuaJit" and ("knucleotide" in file_path):
                continue

            if l.name == "Ruby2" and ("knucleotide" in file_path or "nbody" in file_path):
                continue

            if l.extension == file_extension:
                
                print(f"Running test {l.name}-{root[2:]}\tExecutions: {EXECUTIONS[root[2:]]}\tTest size: {TEST_NUMBER}")
                
                real_times = []
                user_times = []
                sys_times = []

                for i in range(0, TEST_NUMBER):
                    real, user, sys_ = l.time_run(file_path, EXECUTIONS[root[2:]])
                    #print(res)
                    real_times.append(real)
                    user_times.append(user)
                    sys_times.append(sys_)

                time_info["Language"].append(l.name)
                time_info["Test Name"].append(root[2:])
                time_info["Real Mean Time"].append(np.mean(real_times))
                time_info["User Mean Time"].append(np.mean(user_times))
                time_info["Sys Mean Time"].append(np.mean(sys_times))
                time_info["Real Var Time"].append(np.var(real_times))
                time_info["User Var Time"].append(np.var(user_times))
                time_info["Sys Var Time"].append(np.var(sys_times))
                time_info["Executions"].append(EXECUTIONS[root[2:]])
                time_info["Test Size"].append(TEST_NUMBER)

results = pd.DataFrame(time_info)

print(results)
results.to_csv("aaaaaa.csv")

#results.to_csv("jit_results_sync.csv")

# results.to_csv("jit_results_no_sync.csv")