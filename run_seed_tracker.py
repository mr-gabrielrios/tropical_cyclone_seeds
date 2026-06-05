import argparse
import os
import subprocess

def main(dirname: str,
         start_year: int,
         end_year: int):

    bash_string = f'''#!/usr/bin/env bash

# Script to run an array of seed tracking scripts in parallel.
# Gabe Rios (gr7610@princeton.edu)

#SBATCH --nodes=1          # node count
#SBATCH --ntasks=1         # total number of tasks across all nodes
#SBATCH --cpus-per-task=1  # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=32G  # memory per cpu-core (4G is default)
#SBATCH --time=01:01:00    # total run time limit (HH:MM:SS)
#SBATCH --array={start_year}-{end_year}#%24
#SBATCH --mail-type=all    # send email on job start, end and fault
#SBATCH --mail-user=gr7610@princeton.edu

year=$SLURM_ARRAY_TASK_ID

script_pathname=/scratch/gpfs/GEOCLIM/gr7610/tiger3/tools/tropical_cyclone_seeds/tracker.py

# The `-u` flag is used to print Python print statements to the log
python -u $script_pathname {dirname} $year $year
'''

    array_script_pathname = '/scratch/gpfs/GEOCLIM/gr7610/tiger3/tools/tropical_cyclone_seeds/bash/job-track_seeds.sh'
    with open(array_script_pathname, 'w') as f:
        f.write(bash_string)
    os.chmod(array_script_pathname, 0o755)

    subprocess.run(['sbatch', array_script_pathname])

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("dirname", type=str)
    parser.add_argument("start_year", type=int)
    parser.add_argument("end_year", type=int)

    args = parser.parse_args()

    main(args.dirname, args.start_year, args.end_year)
