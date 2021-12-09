#!/bin/bash
#
#SBATCH --job-name=try_check_date
#SBATCH --cpus-per-task=1
#SBATCH --partition=compute
#SBATCH --time=00:10:00
#SBATCH --mem=2G
#SBATCH --output=/data/mackanholt_lab/yp/git_DAM/DAM/DAM_blips_package/output/preview/preview.%j.out
#SBATCH --error=/data/mackanholt_lab/yp/git_DAM/DAM/DAM_blips_package/output/error/error.%j.err
#SBATCH --mail-type=END
#SBATCH --mail-user=yp@clemson.edu

# Users, input variables:

wkdir="/data/mackanholt_lab/yp/git_DAM/DAM/DAM_blips_package/scripts"
cd ${wkdir}

# Enter conda environment with python 3.9
source /opt/ohpc/pub/Software/anaconda3/etc/profile.d/conda.sh
conda activate snakemake

python3 ${wkdir}/blips_script.py \
-s '21 Jul 20' \
-e '16 Jul 20'
