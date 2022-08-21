#Import packages
import getopt, sys
import pandas as pd
import os
from pathlib import Path

#Set to display all columns
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', None)

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


#Read in dead flies file.txt 
with open(dead_flies_file) as f:
    lines = [line.rstrip() for line in f]

#Remove dead flies based on the file 'Deadflies'
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
    sep_condition = df["Condition"].str.split("_", expand = True)
    #changing column names
    sep_condition.columns = columns.split("_")
    df = df.drop(columns = "Condition")
    df = df.merge(sep_condition, left_index=True, right_index=True)
    return df

#Create filters: sleep vs activity, day vs night
sleep = (boutdf['sleep_counts'] == 1) & (boutdf['bout_length'] >= 5)
activity = boutdf['sleep_counts'] == 0
#split up day and night
day = boutdf['Dec_ZT_time'] <720
night = boutdf['Dec_ZT_time'] >= 720

#Create a function for counting bouts 
def bout_count(df_boutdf, ref_boutdf, ref_locomotor):
    #Getting all channel names
    unique_name = ref_boutdf[['Channel', 'Condition']].drop_duplicates()
    #Count bout in each group
    count = df_boutdf.groupby(['Channel', 'Condition'])['bout'].count()
    #Count the number of experiemnt days in each group
    date = ref_locomotor.groupby(['Channel', 'Condition'])['date'].nunique()
    #Take average of count throughout each day
    bout_count_df = (count/date).to_frame().reset_index()
    #Rename the average value column to "Bout_Count" by column index, cannot change order
    bout_count_df = bout_count_df.rename(columns={bout_count_df.columns[2]: 'Bout_Count'})
    #Fill nan value with 0
    bout_count = pd.merge(bout_count_df, unique_name, left_on= ['Channel','Condition'], right_on=['Channel','Condition'],how='right').fillna(0)
    #Seperate condition
    bout_count = sep_condition(bout_count)
    return(bout_count)

#Create a function for counting bout lenghts
def bout_length_compiled(df_boutdf, ref_boutdf, ref_locomotor):
    unique_name = ref_boutdf[['Channel', 'Condition']].drop_duplicates()
    activity_sum = df_boutdf.groupby(['Channel', 'Condition'])['bout_length'].sum()
    date = ref_locomotor.groupby(['Channel', 'Condition'])['date'].nunique()
    activity_mean = (activity_sum/date).to_frame().reset_index()
    bout_length = pd.merge(activity_mean, unique_name, left_on= ['Channel','Condition'], right_on=['Channel','Condition'],how='right').fillna(0)
    Ind_activity_bout_nodead_compiled = bout_length.rename(columns = {0:"Bout_Length"})
    Ind_activity_bout_nodead_compiled = sep_condition(Ind_activity_bout_nodead_compiled)
    return(Ind_activity_bout_nodead_compiled)


#Apply filter, functions to appropriate csv files to generate output csv files
Ind_day_night_sleep_nodead = sep_condition(day_night_sleep_nodead).drop(['Unnamed: 0'], axis = 1)
Ind_day_sleep_nodead = Ind_day_night_sleep_nodead[Ind_day_night_sleep_nodead['Light_status'] == 'Day']
Ind_night_sleep_nodead = Ind_day_night_sleep_nodead[Ind_day_night_sleep_nodead['Light_status'] == 'Night']


#Bout count:
Ind_sleep_bout_nodead_counts_compiled = bout_count(boutdf[sleep], boutdf, locomotor_nodead)
Ind_sleep_bout_nodead_bout_counts_day_compiled = bout_count(boutdf[sleep & day], boutdf, locomotor_nodead)
Ind_sleep_bout_nodead_counts_night_compiled = bout_count(boutdf[sleep & night], boutdf, locomotor_nodead)
Ind_activity_bout_nodead_counts_compiled = bout_count(boutdf[activity], boutdf, locomotor_nodead)
Ind_activity_bout_nodead_counts_day_compiled = bout_count(boutdf[activity & day], boutdf, locomotor_nodead)
Ind_activity_bout_nodead_counts_night_compiled = bout_count(boutdf[activity & night], boutdf, locomotor_nodead)

#Bout length:
Ind_sleep_bout_nodead_boutlength5_compiled = bout_length_compiled(boutdf[sleep], boutdf, locomotor_nodead)
Ind_sleep_bout_nodead_boutlength5_night_compiled = bout_length_compiled(boutdf[sleep & night], boutdf, locomotor_nodead)
Ind_sleep_bout_nodead_boutlength5_day_compiled = bout_length_compiled(boutdf[sleep & day], boutdf, locomotor_nodead)
Ind_activity_bout_nodead_compiled = bout_length_compiled(boutdf[activity], boutdf, locomotor_nodead)
Ind_activity_bout_nodead_day_compiled = bout_length_compiled(boutdf[activity & day], boutdf, locomotor_nodead)
Ind_activity_bout_nodead_night_compiled = bout_length_compiled(boutdf[activity & night], boutdf, locomotor_nodead)

#Locomotor:
Ind_daily_locomotor_activity_data_nodead_compiled = bout_length_compiled(locomotor_nodead, boutdf, locomotor_nodead).rename(columns = {"Bout_Length":"Activity"})
locomotor_prev = Ind_daily_locomotor_activity_data_nodead_compiled.sort_values(by=['Activity'], ascending = False)

#Store the dataframes into a list for iteration
my_list = [Ind_day_night_sleep_nodead,
     Ind_day_sleep_nodead,
     Ind_night_sleep_nodead,
     Ind_sleep_bout_nodead_counts_compiled,
     Ind_sleep_bout_nodead_bout_counts_day_compiled,
     Ind_sleep_bout_nodead_counts_night_compiled,
     Ind_activity_bout_nodead_counts_compiled,
     Ind_activity_bout_nodead_counts_day_compiled,
     Ind_activity_bout_nodead_counts_night_compiled,
     Ind_sleep_bout_nodead_boutlength5_compiled,
     Ind_sleep_bout_nodead_boutlength5_night_compiled,
     Ind_sleep_bout_nodead_boutlength5_day_compiled,
     Ind_activity_bout_nodead_compiled,
     Ind_activity_bout_nodead_day_compiled,
     Ind_activity_bout_nodead_night_compiled,
     locomotor_prev]

files = ["Ind_day_night_sleep_nodead",
         "Ind_day_sleep_nodead",
         "Ind_night_sleep_nodead",
         "Ind_sleep_bout_nodead_counts_compiled",
         "Ind_sleep_bout_nodead_counts_day_compiled", 
         "Ind_sleep_bout_nodead_counts_night_compiled",
         "Ind_activity_bout_nodead_counts_compiled",
         "Ind_activity_bout_nodead_counts_day_compiled",
         "Ind_activity_bout_nodead_counts_night_compiled",
         "Ind_sleep_bout_nodead_boutlength5_compiled",
         "Ind_sleep_bout_nodead_boutlength5_night_compiled",
         "Ind_sleep_bout_nodead_boutlength5_day_compiled",
         "Ind_activity_bout_nodead_compiled",
         "Ind_activity_bout_nodead_day_compiled",
         "Ind_activity_bout_nodead_night_compiled",
         "Ind_daily_locomotor_activity_data_nodead_compiled"]

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

