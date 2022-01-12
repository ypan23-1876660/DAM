INSTRUCTIONS
------------

1. Upload all the raw data files into "data" folder

2. Change the variables in shell script. Modify the variables in <>


        #!/bin/bash
        #SBATCH --job-name=<job name>
        #SBATCH --cpus-per-task=1
        #SBATCH --partition=compute
        #SBATCH --time=<time> (estimated time to execute the script: 5 seconds)
        #SBATCH --mem=<memory> (2G is sufficient)
        #SBATCH --output=<working directory>/DAM/trunk/longitudinal/output/preview/<job name>.%j.out
        #SBATCH --error=<working directory>/DAM/trunk/longitudinal/output/error/<job name>.%j.err
        #SBATCH --mail-type=<type>
        #SBATCH --mail-user=<user email>
   

3. Change Users, input variables: ("\\" for break between lines)

        wkdir="<working directory>"
        cd ${wkdir}

        #Enter conda environment with python 3.9

        source /opt/ohpc/pub/Software/anaconda3/etc/profile.d/conda.sh
        conda activate snakemake

        python3 ${wkdir}/dam_script.py
        --f1 Individual_day_night_sleep.csv \
        --f2 Individual_sleep_activity_bout_data.csv \
        --f3 Individual_daily_locomotor_activity_data.csv \
        --d4 deadflies.txt \
        -c <Condition> 

---

##### EXAMPLE for 2 and 3:
        
        #!/bin/bash
        #
        #SBATCH --job-name=*test1*
        #SBATCH --cpus-per-task=1
        #SBATCH --partition=compute
        #SBATCH --time=*00:10:00*
        #SBATCH --mem=*2G*
        #SBATCH --output=*/data/mackanholt_lab/jp/*DAM/trunk/longitudinal/output/preview/preview.%j.out
        #SBATCH --error=*/data/mackanholt_lab/jp/*/DAM/trunk/longitudinal/output/error/error.%j.err
        #SBATCH --mail-type=END
        #SBATCH --mail-user=*ypp@clemson.edu*


        # Users, input variables:
        wkdir="*/data/mackanholt_lab/jp*/DAM/trunk/longitudinal/scripts"
        cd ${wkdir}

        # Enter conda environment with python 3.9
        source /opt/ohpc/pub/Software/anaconda3/etc/profile.d/conda.sh
        conda activate snakemake

        python3 ${wkdir}/longitudinal_script.py \
        --f1 *Individual_day_night_sleep.csv* \
        --f2 *Individual_sleep_activity_bout_data.csv* \
        --f3 *Individual_daily_locomotor_activity_data.csv* \
        --d4 *031_deadflies.txt* \
        -c *No_Sex_Rep* \
    