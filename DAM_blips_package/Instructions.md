INSTRUCTIONS
------------

1. Upload all the raw data files into "data" folder

2. Change the variables in shell script. Modify the variables in <>

        #!/bin/bash
        #
        #SBATCH --job-name=<job name>
        #SBATCH --cpus-per-task=1
        #SBATCH --partition=compute
        #SBATCH --time=<time> (estimated time to execute the script: 5 seconds)
        #SBATCH --mem=<memory> (2G is sufficient)
        #SBATCH --output=<working directory>/DAM/trunk/DAM_blips_package/output/preview/<job name>.%j.out
        #SBATCH --error=<working directory>/DAM/trunk/DAM_blips_package/output/error/<job name>.%j.err
        #SBATCH --mail-type=<type>
        #SBATCH --mail-user=<user email>

3. Change Users, input variables: ("\\" for break between lines)

        wkdir="<working directory>"
        cd ${wkdir}
        
        # Enter conda environment with python 3.9
        source /opt/ohpc/pub/Software/anaconda3/etc/profile.d/conda.sh
        conda activate snakemake
        
        python3 ${wkdir}/blips_script.py
        -s 'start date' \
        -o 'end date' 

---

##### EXAMPLE for 2 and 3:

    #!/bin/bash
    #
    #SBATCH --job-name=Trial1
    #SBATCH --cpus-per-task=1
    #SBATCH --partition=compute
    #SBATCH --time=00:10:00
    #SBATCH --mem=2G
    #SBATCH --output=/path/to/project_directory/DAM/trunk/DAM_blips_package/output/preview/preview.%j.out
    #SBATCH --error=/path/to/project_directory/DAM/trunk/DAM_blips_package/output/error/error.%j.err
    #SBATCH --mail-type=END
    #SBATCH --mail-user=username@clemson.edu

    # Users, input variables:
    wkdir="/path/to/project_directory/DAM/trunk/DAM_blips_package"
    cd ${wkdir}
    
    # Enter conda environment with python 3.9
    source /opt/ohpc/pub/Software/anaconda3/etc/profile.d/conda.sh
    conda activate snakemake
    
    python3 ${wkdir}/blips_script.py \
    -s '30 Sep 20' \
    -o '6 Oct 20'  
    
4. Navigate to "/path/to/project_directory/DAM/trunk/DAM_blips_package/scripts" 
5. Run `sbatch blips_initiator.sh`
