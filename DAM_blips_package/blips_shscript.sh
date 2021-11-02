#!/bin/bash
#
#SBATCH --job-name=Launch2
#SBATCH --cpus-per-task=1
#SBATCH --partition=compute
#SBATCH --time=00:10:00
#SBATCH --mem=2G
#SBATCH --output=/data/mackanholt_lab/yp/dev_DAM/DAM_blips_package/output/preview/preview.%j.out
#SBATCH --error=/data/mackanholt_lab/yp/dev_DAM/DAM_blips_package/output/error/error.%j.err
#SBATCH --mail-type=END
#SBATCH --mail-user=yp@clemson.edu

# Users, input variables:

cd /data/mackanholt_lab/yp/dev_DAM/DAM_blips_package

python3 /data/mackanholt_lab/yp/dev_DAM/DAM_blips_package/blips_script.py \
-s '30 Sep 20' \
-e '6 Oct 20' \

