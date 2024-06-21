#!/usr/bin/env python3

import numpy as np
import time
import os
import shutil
import subprocess
import threading
import queue
import argparse


# ... Initialization and Setup

# Path to the 42 executable
run_path = '/42' 

threads_running = True


# List of files to keep from each run
# Keep output files of interest, modified input files, and the stdout/stderr files
save_list = ['time.42', 'wbn.42', 'PosN.42',
             'SC_Simple.txt', 'SettleTime.txt', 
             'stdout.txt', 'stderr.txt']




################################################################################


def RunMC():
    ''' Run a Monte Carlo campaign  
        Spawns args.num_cores threads to run args.num_runs simulations
        Also handles some one-time setup tasks
    '''
    global threads_running
    
    template_dir = os.path.abspath(args.template)
    output_dir = os.path.abspath(args.outdir)
    num_runs = args.num_runs
    num_cores = args.num_cores

    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create the template directory if it does not exist
    if not os.path.exists(template_dir):
        print('Creating template from /42/InOut')
        shutil.copytree('/42/InOut', template_dir)

    # Make sure graphics front end is FALSE
    SimPath = os.path.join(template_dir, 'Inp_Sim.txt')
    ReplaceLineInFile(SimPath, 7, 'FALSE                           !  Graphics Front End?')

    # Start the campaign timer
    start_time = time.time()
    
    # Queue for dispatching jobs to threads
    job_queue = queue.Queue()
    threads = []
    
    # Spawn one thread per core, passing it the queue
    for i in range(num_cores):
        t = threading.Thread(target=runner, args=(job_queue,))
        t.start()
        threads.append(t)

    # Number of digits in the run number 
    num_dig = int(np.floor(np.log10(num_runs))) + 1
    
    # Queue up path for each run
    for i in range(args.index, args.index + num_runs):
        path = os.path.join(output_dir, f'Run_{i:0{num_dig}}')
        job_queue.put(path)

    # Wait for all jobs to be completed
    job_queue.join()
    
    # Signal threads to stop
    threads_running = False

    # Wait for all threads to finish
    for i in range(num_cores):
        threads[i].join()

    print(f'Campaign Duration: {time.time() - start_time : .03f} sec')




################################################################################
### This script is based on the Julia script RunMC.jl 
### The multiprocessing architecture has been changed to ensure all cores are used


def runner(job_queue):
    ''' Thread entry point for running jobs
        Each thread waits for available jobs and then spawns a new process to run the job
        path is placed in queue by the main thread
    '''

    while threads_running:
        try:
            
            # Absolute path to job folder
            path = job_queue.get(timeout=0.01)

            ### For each run....
            
            t = time.time()

            if args.debug:
                print(f'Running {path}')

            # Delete old data folder if it exists
            if os.path.exists(path):
                shutil.rmtree(path)

            # Copy template to data folder
            shutil.copytree(args.template, path)


            if args.debug:
                print(f'Preprocessing {path}')
    
            # Customize input files
            preprocess(path)


            # Redirect stdout and stderr to files
            so = os.path.join(path, 'stdout.txt')
            se = os.path.join(path, 'stderr.txt')


            if args.debug:
                print(f'Running 42 {path}')

            exe = os.path.join(run_path, '42')
            p = subprocess.Popen(f'{exe} ../{path}', cwd=run_path, shell=True,
                                 stdout=open(so, 'w'), stderr=open(se, 'w'))
            p.wait()

            if args.debug:
                print(f'Postprocessing {path}')
    
            postprocess(path)

            if args.compress:
                if args.debug:
                    print(f'Compressing {path}')
                
                # the path directory's parent dir
                parent = os.path.dirname(path)
                base = os.path.basename(path)

                p = subprocess.Popen(f'tar -czf {path}.tar.gz -C {parent} {base}', shell=True,
                                       stdout=subprocess.DEVNULL,
                                       stderr=subprocess.STDOUT)
                p.wait()
                # Delete the folder
                shutil.rmtree(path)

            print(f'Finished {path} in {time.time() - t : .03f} sec')

        except queue.Empty:
            continue

        # Print any exceptions
        except Exception as e:
            print(e)

        job_queue.task_done()
    


def preprocess(path):

    ''' Customize the input files for each run
        path: str, path to the inputs folder
    '''

    # Ranomize initial attitude
    EulAng = 20 * (2 * np.random.rand(3) - 1)

    s = f'{EulAng[0]:03f} {EulAng[1]:03f} {EulAng[2]:03f}    213      ! Angles (deg) & Euler Sequence'

    ReplaceLineInFile(os.path.join(path, 'SC_Simple.txt'), 16, s)



def postprocess(path):
    ''' Post-process the results of each run
        path: str, path to the run folder
    '''

    ##### Do any desired calculations #####
    # I prefer to do data processing in a separate script, but it can be done here as well

    
    # Delete any non-saved files
    if not args.keep:
        files = os.listdir(path)
        for f in files:
            if f not in save_list:
                os.remove(os.path.join(path, f))

    








def ReplaceLineInFile(FileName, LineNum, text):
    ''' Replace a line in a file
        FileName: str, path to the file
        LineNum: int, line number to replace (1-based)
        text: str, text to replace the line with    
    '''
    with open(FileName, 'r') as file:
        lines = file.readlines()

    lines[LineNum-1] = text + '\n'

    with open(FileName, 'w') as file:
        file.writelines(lines)





if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run a Monte Carlo campaign')
    parser.add_argument('-d', '--debug',     action='store_true',               help='Print debug info')
    parser.add_argument('-k', '--keep',      action='store_true',               help='Keep all files (default is to keep only the files in save_list)')
    parser.add_argument('-z', '--compress',  action='store_true',               help='Compress the resulting data file')
    parser.add_argument('-i', '--index',     type=int, default=0,               help='Index of first run (good for distributed runs)')
    parser.add_argument('-n', '--num_runs',  type=int, default=10,              help='Number of runs to perform')
    parser.add_argument('-c', '--num_cores', type=int, default=10,              help='Number of cores to use')
    parser.add_argument('-t', '--template',  type=str, default='testsc',        help='Path to the template dir (will be created if it does not exist)')
    parser.add_argument('-o', '--outdir',    type=str, default='mc_data',       help='Path to output the data (each run will be subfolder in this dir)')
    args = parser.parse_args()


    RunMC()


# ./monte_carlo.py -n 100 -c 16
# Campaign Duration:  36.856 sec

# ./monte_carlo.py -n 100 -c 16 -z
# Campaign Duration:  37.742 sec