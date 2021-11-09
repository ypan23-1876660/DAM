<<<<<<< HEAD:DAM_streamline_package/Instructions.MD
##INSTRUCTIONS:
=======
INSTRUCTIONS
------------
>>>>>>> f299af3657149cb5fac42ec304b8f19baee6932b:DAM_streamline_package/Instructions.md

1. Upload all the raw data files into "data" folder

2. Rename the files accordingly to:
"Individual_day_night_sleep.csv"
"Individual_sleep_activity_bout_data.csv"
"Individual_daily_locomotor_activity_data.csv"
"deadflies.txt"


3. Change the variables in shell script. Modify the variables in <>
`
#!/bin/bash
#
#SBATCH --job-name=<job name>
#SBATCH --cpus-per-task=1
#SBATCH --partition=compute
#SBATCH --time=<time> (estimated time to execute the script: 5 seconds)
#SBATCH --mem=<memory> (2G is sufficient)
#SBATCH --output=<working directory>/DAM_streamline_package/output/preview/<job name>.%j.out
#SBATCH --error=<working directory>/DAM_streamline_package/output/error/<job name>.%j.err
#SBATCH --mail-type=<type>
#SBATCH --mail-user=<user email>
`

4. Change Users, input variables:("\" for break between lines)
wkdir="<working directory>"
cd ${wkdir}

# Enter conda environment with python 3.9
source /opt/ohpc/pub/Software/anaconda3/etc/profile.d/conda.sh
conda activate snakemake


python3 ${wkdir}/dam_script.py
--f1 Individual_day_night_sleep.csv \
--f2 Individual_sleep_activity_bout_data.csv \
--f3 Individual_daily_locomotor_activity_data.csv \
--d4 deadflies.txt \
-c <Condition> 



EXAMPLE for 3 and 4:
#!/bin/bash
#
#SBATCH --job-name=Trial1
#SBATCH --cpus-per-task=1
#SBATCH --partition=compute
#SBATCH --time=00:10:00
#SBATCH --mem=2G
#SBATCH --output=/data/mackanholt_lab/yp/git_DAM/DAM/DAM_streamline_package/output/preview/preview.%j.out
#SBATCH --error=/data/mackanholt_lab/yp/git_DAM/DAM/DAM_streamline_package/output/error/error.%j.err
#SBATCH --mail-type=END
#SBATCH --mail-user=ypp@clemson.edu


# Users, input variables:
wkdir="/data/mackanholt_lab/yp/git_DAM/DAM/DAM_streamline_package"
cd ${wkdir}

# Enter conda environment with python 3.9
source /opt/ohpc/pub/Software/anaconda3/etc/profile.d/conda.sh
conda activate snakemake

python3 ${wkdir}/dam_script.py \
--f1 Individual_day_night_sleep.csv \
--f2 Individual_sleep_activity_bout_data.csv \
--f3 Individual_daily_locomotor_activity_data.csv \
--d4 031_deadflies.txt \
-c No_Sex_Rep \
