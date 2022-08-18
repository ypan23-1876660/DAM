README
-------

### Usage: 

Process ShinyR DAM output data for streamline analysis 


### Simplest usage:
1. Navigate to the directory containing the longitudinal scrips: `cd/path/to/directory/streamline/scrips`
2. Run the script: `sbatch streamline_initiator.sh`
    
### Options:
    
  __`-c`__ CONDITION
> **The value of Condition column**
>
> *ShinyR DAM "Condition" column entries that look like "CSB_F_EtOH_2" could correspond to a `-c` of "Line_Sex_Treatment_Rep".
> This would result in the creation of columns corresponding to "Line," "Sex," "Treatment," and "Rep" in the CSV outputted as a result of this script.*
>
> **Format** : 'condition1_condition2_condition3' (Exclude quotations, Include underscore)
>
> *Must match the order of underscore-delimited, user-defined entries in the "Condition" column of the ShinyR DAM output. The underscore-delimited entries will become 
> the respective column names of the output file generated from this script.*
>
> **e.g.** : `Sex_Treatment_Rep`
> 

  __`-f1`__ INPUT FILE
> **Import csv files from ShinyR_outputs: individual_day_night_sleep.csv**
>
> **Format** : 'individual_day_night_sleep.csv'  (Include underscore, Exclude quotations)
>
> *The entered file name must match the uploaded raw data file name*
>
> **e.g.** : `'individual_day_night_sleep.csv'`
   
  __`-f2`__ INPUT FILE
> **Import csv files from ShinyR_outputs: individual_sleep_activity_bout_data.csv**
>
> **Format**: 'individual_sleep_activity_bout_data.csv'  (Include underscore, Exclude quotations)
>
> *The entered file name must match the uploaded raw data file name*
>
> **e.g.**: `'individual_sleep_activity_bout_data.csv'` 

  __`-f3`__ INPUT FILE
> **Import csv files from ShinyR_outputs: individual_daily_locomotor_activity_data.csv**
>
> **Format** : 'individual_daily_locomotor_activity_data.csv' (Include underscore, Exclude quotations)
>
> *The entered file name must match the uploaded raw data file name*
>
> **e.g.** : `'individual_daily_locomotor_activity_data.csv'` 

  __`-f4`__ INPUT FILE
> **Import txt file for dead flies that are removed manually**
>
> **Format** : 'dead_flies.txt' (Include underscore, Exclude quotations)    
>
> *The txt file should contain a list of channel names*
>
> **e.g.** :`'dead_files.txt'`

### Output preview:
- [**Output_file_name**]: Return the first 10 rows of each output csv files 
