READ ME

Usage: Process ShinyR DAM output data for SAS analysis 

Simplest usage:
cd to the folder containing the dam_script.py, run <sbatch dam_shscript.sh>
    
Options:
    -c CONDITION
     seperated conditions by underscore. 
     *Must match the order of underscore-delimited, user-defined entries in the "Condition" column of the ShinyR DAM output. The underscore-delimited entries will become the respective column names of the output file generated from this script.*
     
    E.g. ShinyR DAM "Condition" column entries that look like "CSB_F_EtOH_2" could correspond to a `-c` of "Line_Sex_Treatment_Rep".
    This would result in the creation of columns corresponding to "Line," "Sex," "Treatment," and "Rep" in the CSV outputted as a result of this script.
     *The column order separated by underscores order should be the same as the condition, and is user-defined*

    -o OUTPUT FILE PATH
    path for export output csv files 

    --f1 IMPORT FILE
    import csv files from ShinyR_outputs: individual_day_night_sleep.csv
    *include underscore*
    
    --f2 IMPORT FILE
    import csv files from ShinyR_outputs: individual_sleep_activity_bout_data.csv
    *include underscore*
    
    --f3 IMPORT FILE
    import csv files from ShinyR_outputs: individual_daily_locomotor_activity_data.csv
    *include underscore*
    
    --d4 IMPORT FILE:
    import txt file for dead flies that are removed manually
    the txt file should contain a list of channel names
    *include underscore*


Example: ("\" for break between lines)
    python3 <dam_script.py>\
    --f1 Individual_day_night_sleep.csv \
    --f2 Individual_sleep_activity_bout_data.csv \
    --f3 Individual_daily_locomotor_activity_data.csv \
    --d4 031_deadflies.txt \
    -c Line_Sex_Treatment_Rep \
    -o <output files path>\


Directions: 
    upload --f1, --f2, --f3, --d4 into data folder
    
    job-name = <job-name>
    output= <file path> /DAM_streamline_package/output/<job-name>.%j.out
    error= <file path> /DAM_streamline_package/output/<job-name>.%j.err
    mail-user= <user email> 
    
    python3 <file path>/DAM_streamline_package/dam_script.py 
    -c <condition>
    -o <file path>/DAM_streamline_package/output/output_csv