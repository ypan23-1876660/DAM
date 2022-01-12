#Import packages
import getopt, sys
import pandas as pd
import os
from pathlib import Path

#Set to working directory
cwd = os.getcwd()
p = Path(cwd).parent
os.chdir(str(p) + "/data")

#Read in user variables
argv = sys.argv[1:]
inputfiles = [None]*3
dead_flies_file = None



try:
    opts, args = getopt.getopt(argv, "h:c:", ["f1=","f2=","f3=","d4="])
    
except:
    print("Error")
        
for opt, arg in opts:
    if opt in ['-c']:
        columns = str(arg)
    elif opt in ['--f1']:
        inputfiles[0] = arg
        day_night_sleep = pd.read_csv(str(inputfiles[0]))
    elif opt in ['--f2']:
        inputfiles[1] = arg
        bout_time = pd.read_csv(str(inputfiles[1]))
    elif opt in ['--f3']:
        inputfiles[2] = arg
        locomotor = pd.read_csv(str(inputfiles[2]))
    elif opt in ['--d4']:
        dead_flies_file = str(arg)


#Renameing coloumn "value" in locomotor to "bout length"
locomotor = locomotor.rename(columns = {"variable":"Channel", "value":"bout_length"})


#Remove dead flies across files where locomotor value == 0 
value_zero = locomotor[locomotor['bout_length'] == 0]
nodead = value_zero.drop_duplicates(subset= ['Channel'])
day_night_sleep_nodead = day_night_sleep[~day_night_sleep.Channel.isin(nodead.Channel.values)]
boutdf_nodead = bout_time[~bout_time.Channel.isin(nodead.Channel.values)]
locomotor_nodead = locomotor[~locomotor.Channel.isin(nodead.Channel.values)]


#Read in dead flies file from data folder
with open(dead_flies_file) as f:
    lines = [line.rstrip() for line in f]


#Taking out dead flies from dead flies file
day_night_sleep_nodead = day_night_sleep_nodead[~day_night_sleep_nodead.Channel.isin(lines)]
boutdf_nodead = boutdf_nodead[~boutdf_nodead.Channel.isin(lines)]
locomotor_nodead  = locomotor_nodead [~locomotor_nodead .Channel.isin(lines)]


#Removing last bout length
#rename first column to index
a = boutdf_nodead.rename(columns={boutdf_nodead.columns[0]: 'Index'})
#Select last row of each group (for each unique name)
g = a.groupby('Channel').tail(1)
#Removing last row for each group
boutdf = a[~a.Index.isin(g.Index.values)]


#Create a function for seperating conditions
def sep_condition(df):
    #Splitting value in Condition column by "_"
    sep_condition = df["Condition"].str.split("_", expand = True)
    #Using the splitted values as column names
    sep_condition.columns = columns.split("_")
    #Drop the old Condition column
    df = df.drop(columns = "Condition")
    #Combine all the splitted columns into a dataframe
    df = df.merge(sep_condition, left_index=True, right_index=True)
    return df


#Create filters
#Sleep: If sleep count is 1 and if the sleep bout lenghth is greater than 5
sleep = (boutdf['sleep_counts'] == 1) & (boutdf['bout_length'] >= 5)
#Activity: if the sleep count is 0
activity = boutdf['sleep_counts'] == 0
#Day: If ZT time is less than 720 hours
day = boutdf['Dec_ZT_time'] <720
#Night: If ZT time is equal or greater than 720 hours
night = boutdf['Dec_ZT_time'] >= 720


#Create a function for calculating the sum of bout count
#Input file from raw data: "Individual_sleep_activity_bout_data.csv"
#Input dataframe from this pipiline: "boutdf"
def bout_count_longitudinal(df_boutdf):    
    #Groupby the dataframe "boutdf" by the order of Channel, date, condition
    #Count the total number of bout within each group
    #Convert the series result to dataframe and set the index as each column names
    count = df_bout_df.groupby(['Channel', 'date', 'Condition'])['bout'].count().to_frame().reset_index()
    #Rename the column name bout to Bout Count
    bout_count = count.rename(columns={'bout': 'Bout_Count'})
    #Fill in nan value with 0
    bout_count = bout_count.fillna(0)
    #Split the Condition column into individual column names calling sep_condition function
    bout_count = sep_condition(bout_count)
    return(bout_count)


#Create a function for calculating the sum of bout lenghts
#Input file from raw data: "Individual_sleep_activity_bout_data.csv"
#Input dataframe from this pipiline: "boutdf"
def bout_length_longitudinal(df_boutdf):    
    #Groupby the dataframe "boutdf" by the order of Channel, date, condition
    #Sum the total bout_length in each group from column bout_length 
    #Convert the series result to dataframe and set the index as each column names
    bout_length_sum = df_boutdf.groupby(['Channel', 'date', 'Condition'])['bout_length'].sum().to_frame().reset_index()
    #Rename the column name bout_lenght to Bout_Length
    bout_length_sum = bout_length_sum.rename(columns = {"bout_length":"Bout_Length"})
    #Fill in nan value with 0
    bout_length_sum = bout_length_sum.fillna(0)
    #Split the Condition column into individual column names calling sep_condition function
    bout_length_sum = sep_condition(bout_length_sum)
    return(bout_length_sum)


#Create a function for calculating the sum of sleep for each individual fly
#Input file from raw data: "Individual_day_night_sleep"
#Input dataframe from this pipiline: "day_night_sleep_nodead"
def sleep_per_ind_longitudinal(df_day_night_sleep_nodead):
    #Group by the dataframe "day_night_sleep_nodead" by the order of Channel, Condition, Light_status
    #Sum the total sleep from column mean_sleep_per_ind
    sleep_sum = df_day_night_sleep_nodead.groupby(['Channel', 'Condition', 'Light_status'])['mean_sleep_per_ind'].sum().to_frame().reset_index()
    #Rename the column mean_sleep_per_ind to sum_sleep_per_ind
    sleep_sum = sleep_sum.rename(columns = {"mean_sleep_per_ind":"sum_sleep_per_ind"})
    #Fill in nan value with 0
    sleep_sum = sleep_sum.fillna(0)
    #Split the Condition column into individual column names calling sep_condition function
    sleep_sum = sep_condition(sleep_sum)
    return(sleep_sum)


#Sleep time: Apply filters Day, Night
Ind_day_night_sleep_nodead = sleep_per_ind_longitudinal(day_night_sleep)
Ind_day_sleep_nodead = Ind_day_night_sleep_nodead[Ind_day_night_sleep_nodead['Light_status'] == 'Day']
Ind_night_sleep_nodead = Ind_day_night_sleep_nodead[Ind_day_night_sleep_nodead['Light_status'] == 'Night']



#Bout count sum: Apply filters Day, Night, Activity, Sleep
Ind_sleep_bout_nodead_counts_longitudinal = bout_count_longitudinal(boutdf[sleep])
Ind_sleep_bout_nodead_bout_counts_day_longitudinal = bout_count_longitudinal(boutdf[sleep & day])
Ind_sleep_bout_nodead_counts_night_longitudinal = bout_count_longitudinal(boutdf[sleep & night])
Ind_activity_bout_nodead_counts_longitudinal = bout_count_longitudinal(boutdf[activity])
Ind_activity_bout_nodead_counts_day_longitudinal = bout_count_longitudinal(boutdf[activity & day])
Ind_activity_bout_nodead_counts_night_longitudinal = bout_count_longitudinal(boutdf[activity & night])




#Bout length sum: Apply filters Day, Night, Activity, Sleep
Ind_sleep_bout_nodead_boutlength5_longitudinal = bout_length_longitudinal(boutdf[sleep])
Ind_sleep_bout_nodead_boutlength5_night_longitudinal = bout_length_longitudinal(boutdf[sleep & night])
Ind_sleep_bout_nodead_boutlength5_day_longitudinal = bout_length_longitudinal(boutdf[sleep & day])
Ind_activity_bout_nodead_longitudinal = bout_length_longitudinal(boutdf[activity])
Ind_activity_bout_nodead_day_longitudinal = bout_length_longitudinal(boutdf[activity & day])
Ind_activity_bout_nodead_night_longitudinal = bout_length_longitudinal(boutdf[activity & night])



#Locomotor activity:
#Rename column bout_lenghth to Activity
Ind_daily_locomotor_activity_data_nodead = sep_condition(locomotor_nodead).rename(columns = {"bout_length":"Activity"})
#Sorted the values by Activity from highest to lowest for preview
locomotor_prev = Ind_daily_locomotor_activity_data_nodead.sort_values(by=['Activity'], ascending = False)



#Store the dataframes into a list for iteration
my_list = [Ind_day_night_sleep_nodead,
     Ind_day_sleep_nodead,
     Ind_night_sleep_nodead,
     Ind_sleep_bout_nodead_counts_longitudinal,
     Ind_sleep_bout_nodead_bout_counts_day_longitudinal,
     Ind_sleep_bout_nodead_counts_night_longitudinal,
     Ind_activity_bout_nodead_counts_longitudinal,
     Ind_activity_bout_nodead_counts_day_longitudinal,
     Ind_activity_bout_nodead_counts_night_longitudinal,
     Ind_sleep_bout_nodead_boutlength5_longitudinal,
     Ind_sleep_bout_nodead_boutlength5_night_longitudinal,
     Ind_sleep_bout_nodead_boutlength5_day_longitudinal,
     Ind_activity_bout_nodead_longitudinal,
     Ind_activity_bout_nodead_day_longitudinal,
     Ind_activity_bout_nodead_night_longitudinal,
     locomotor_prev]



files = ["Ind_day_night_sleep_nodead",
         "Ind_day_sleep_nodead",
         "Ind_night_sleep_nodead",
         "Ind_sleep_bout_nodead_counts_longitudinal",
         "Ind_sleep_bout_nodead_counts_day_longitudinal", 
         "Ind_sleep_bout_nodead_counts_night_longitudinal",
         "Ind_activity_bout_nodead_counts_longitudinal",
         "Ind_activity_bout_nodead_counts_day_longitudinal",
         "Ind_activity_bout_nodead_counts_night_longitudinal",
         "Ind_sleep_bout_nodead_boutlength5_longitudinal",
         "Ind_sleep_bout_nodead_boutlength5_night_longitudinal",
         "Ind_sleep_bout_nodead_boutlength5_day_longitudinal",
         "Ind_activity_bout_nodead_longitudinal",
         "Ind_activity_bout_nodead_day_longitudinal",
         "Ind_activity_bout_nodead_night_longitudinal",
         "Ind_daily_locomotor_activity_data_nodead_longitudinal"]


#Set output file path
os.chdir(str(p) + "/output/output_csv")

#Print channel name of dead flies that are removed by value == 0
print("Remove Dead Flies")
print(nodead)


#Print preview for each csv file and export csv file to output file path 
files = [x + ".csv" for x in files]
combine = dict(zip(files, my_list))
for key, value in combine.items():
    print(key)
    print(value.head(10))
    value.to_csv(key)