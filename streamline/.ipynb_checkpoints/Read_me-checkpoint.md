READ ME
-------

Usage: Process ShinyR DAM output data for SAS analysis 

Simplest usage:
cd to the folder containing the dam_script.py, run <sbatch dam_shscript.sh>
    
Options:
    -c CONDITION
     seperated "conditions" column by underscore. 
     *Must match the order of underscore-delimited, user-defined entries in the "Condition" column of the ShinyR DAM output. The underscore-delimited entries will become the respective column names of the output file generated from this script.*
     
    E.g. ShinyR DAM "Condition" column entries that look like "CSB_F_EtOH_2" could correspond to a `-c` of "Line_Sex_Treatment_Rep".
    This would result in the creation of columns corresponding to "Line," "Sex," "Treatment," and "Rep" in the CSV outputted as a result of this script.


    --f1 INPUT FILE
    Import csv files from ShinyR_outputs: individual_day_night_sleep.csv
    *include underscore*
    
    --f2 INPUT FILE
    import csv files from ShinyR_outputs: individual_sleep_activity_bout_data.csv
    *include underscore*
    
    --f3 INPUT FILEs
    import csv files from ShinyR_outputs: individual_daily_locomotor_activity_data.csv
    *include underscore*
    
    --d4 INPUT FILE:
    import txt file for dead flies that are removed manually
    the txt file should contain a list of channel names
    *include underscore*

Output preview:
    [output_csv]: Return the first 10 rows of each output csv files 