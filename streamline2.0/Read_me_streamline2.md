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

### Output preview: Return the first 10 rows of each output csv files
[***Day_night_sleep***]: Return the mean sleep per individual 
- [**Ind_day_night_sleep_nodead**]: day and night together
- [**Ind_day_sleep_nodead**]: day only
- [**Ind_night_sleep_nodead**]: night only

- [**Ind_sleep_bout_nodead_counts_compiled**]: Return the *average sleep bout count* for an individual calculated by averaging all bout counts across the total experimental timeframe
- [**Ind_sleep_bout_nodead_bout_counts_day_compiled**]: Return the *average sleep bout count* for an individual across total experimental days for *day*
- [**Ind_sleep_bout_nodead_counts_night_compiled**]: Return the *average sleep bout count* for an individual across total experimental days for *night*  

- [**Ind_activity_bout_nodead_counts_compiled**]: Return the *average activity bout count* for an individual across total experimental days for *day and night*
- [**Ind_activity_bout_nodead_counts_day_compiled**]: Return the *average activity bout count* for an individual across total experimental days for *day*
- [**Ind_activity_bout_nodead_counts_night_compiled**]: Return the *avaerage activity bout count* for an individual across total experimental days for *night*  

- [**Ind_sleep_bout_nodead_boutlength5_compiled**]: Return the *average sleep bout length* for an individual calculated by averaging the daily bout length across all days for *day and night*
- [**Ind_sleep_bout_nodead_boutlength5_day_compiled**]: Return the *average sleep bout length* for an individual across each date entry for *day*
- [**Ind_sleep_bout_nodead_boutlength5_night_compiled**]: Return the *average sleep bout length* for an individual across each date entry for *night*  

- [**Ind_activity_bout_nodead_compiled**]: Return the *average activity bout length* for an individual across each date entry for *day and night*
- [**Ind_activity_bout_nodead_day_compiled**]: Return the *average activity bout length* for an individual across each date entry for *day*
- [**Ind_activity_bout_nodead_night_compiled**]: Return the *average activity bout length* for an individual across each date entry for *night*  

- [**locomotor_prev**]: Return the *average locomotor activity* (counts per day) for an individual across the total experimental timeframe for *day and night*

     