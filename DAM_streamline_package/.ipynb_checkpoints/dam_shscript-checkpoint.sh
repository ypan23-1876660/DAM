#!/bin/bash
#
#SBATCH --job-name=try2
#SBATCH --cpus-per-task=1
#SBATCH --partition=compute
#SBATCH --time=00:10:00
#SBATCH --mem=2G
#SBATCH --output=/data/mackanholt_lab/yp/git_DAM/DAM/DAM_streamline_package/output/preview/preview.%j.out
#SBATCH --error=/data/mackanholt_lab/yp/git_DAM/DAM/DAM_streamline_package/output/error/error.%j.err
#SBATCH --mail-type=END
#SBATCH --mail-user=yp@clemson.edu

# Users, input variables:

cd /data/mackanholt_lab/yp/git_DAM/DAM/DAM_streamline_package

python3 /data/mackanholt_lab/yp/git_DAM/DAM/DAM_streamline_package/dam_script.py \
--f1 Individual_day_night_sleep.csv \
--f2 Individual_sleep_activity_bout_data.csv \
--f3 Individual_daily_locomotor_activity_data.csv \
--d4 031_deadflies.txt \
-c No_Sex_Rep \

