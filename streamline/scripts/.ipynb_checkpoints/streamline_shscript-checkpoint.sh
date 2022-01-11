#!/bin/bash
#
#SBATCH --job-name=try2
#SBATCH --cpus-per-task=1
#SBATCH --partition=compute
#SBATCH --time=00:10:00
#SBATCH --mem=2G
#SBATCH --output=/data/mackanholt_lab/yp/git_DAM/DAM/streamline/output/preview/preview.%j.out
#SBATCH --error=/data/mackanholt_lab/yp/git_DAM/DAM/streamline/output/error/error.%j.err
#SBATCH --mail-type=END
#SBATCH --mail-user=user@clemson.edu

# Users, input variables:

wkdir="/data/mackanholt_lab/yp/git_DAM/DAM/streamline/scripts"
cd ${wkdir}

# Enter conda environment with python 3.9
source /opt/ohpc/pub/Software/anaconda3/etc/profile.d/conda.sh
conda activate snakemake

python3 ${wkdir}/streamline_script.py \
--f1 Individual_day_night_sleep.csv \
--f2 Individual_sleep_activity_bout_data.csv \
--f3 Individual_daily_locomotor_activity_data.csv \
--d4 031_deadflies.txt \
-c No_Sex_Rep 

