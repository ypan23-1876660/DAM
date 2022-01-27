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
#Delete the parts for merge, drop duplicates, because we just need the Condition for Channel name
def bout_count_longitudinal(df_bout_df):    
    count = df_bout_df.groupby(['Channel', 'date', 'Condition'])['bout'].count().to_frame().reset_index()
    #Rename bout to Bout Count
    bout_count = count.rename(columns={'bout': 'Bout_Count'})
    bout_count = bout_count.fillna(0)
    bout_count = sep_condition(bout_count)
    return(bout_count)


#Create a function for counting bout lenghts
#Delete the parts for merge, drop duplicates, because we just need the Condition for Channel name
def bout_length_longitudinal(df_boutdf):    
    bout_length_mean = df_boutdf.groupby(['Channel', 'date', 'Condition'])['bout_length'].mean().to_frame().reset_index()
    bout_length_mean = sep_condition(bout_length_mean)
    bout_length_mean = bout_length_mean.fillna(0)
    bout_length_mean = bout_length_mean.rename(columns = {"bout_length":"Bout_Length"})
    return(bout_length_mean)


#Delete the parts for merge, drop duplicates, because we just need the Condition for Channel name
def sum_sleep_per_ind_day_OR_night(df_boutdf):
    bout_length_sum = df_boutdf.groupby(['Channel', 'Condition', 'date'])['bout_length'].sum().to_frame().reset_index()
    proportion = bout_length_sum['bout_length']/720
    bout_length_sum['sum_sleep_per_ind'] = proportion
    bout_length_sum = sep_condition(bout_length_sum)
    bout_length_sum = bout_length_sum.fillna(0)
    bout_length_sum = bout_length_sum.drop(columns = "bout_length")
    return(bout_length_sum)

def sum_sleep_per_ind_day_AND_night(df_boutdf):    
    bout_length_sum = boutdf[sleep].groupby(['Channel', 'Condition', 'date'])['bout_length'].sum().to_frame().reset_index()
    proportion = bout_length_sum['bout_length']/1440
    bout_length_sum['sum_sleep_per_ind'] = proportion
    bout_length_sum = sep_condition(bout_length_sum)
    bout_length_sum = bout_length_sum.fillna(0)
    bout_length_sum = bout_length_sum.drop(columns = "bout_length")
    return(bout_length_sum)


#Sleep time calculate:
Ind_day_night_sleep_nodead = sum_sleep_per_ind_day_AND_night(boutdf[sleep])
Ind_day_sleep_nodead = sum_sleep_per_ind_day_OR_night(boutdf[sleep & day])
Ind_night_sleep_nodead = sum_sleep_per_ind_day_OR_night(boutdf[sleep & night])



#Bout count:
Ind_sleep_bout_nodead_counts_longitudinal = bout_count_longitudinal(boutdf[sleep])
Ind_sleep_bout_nodead_bout_counts_day_longitudinal = bout_count_longitudinal(boutdf[sleep & day])
Ind_sleep_bout_nodead_counts_night_longitudinal = bout_count_longitudinal(boutdf[sleep & night])
Ind_activity_bout_nodead_counts_longitudinal = bout_count_longitudinal(boutdf[activity])
Ind_activity_bout_nodead_counts_day_longitudinal = bout_count_longitudinal(boutdf[activity & day])
Ind_activity_bout_nodead_counts_night_longitudinal = bout_count_longitudinal(boutdf[activity & night])




#Bout length:
Ind_sleep_bout_nodead_boutlength5_longitudinal = bout_length_longitudinal(boutdf[sleep])
Ind_sleep_bout_nodead_boutlength5_night_longitudinal = bout_length_longitudinal(boutdf[sleep & night])
Ind_sleep_bout_nodead_boutlength5_day_longitudinal = bout_length_longitudinal(boutdf[sleep & day])
Ind_activity_bout_nodead_longitudinal = bout_length_longitudinal(boutdf[activity])
Ind_activity_bout_nodead_day_longitudinal = bout_length_longitudinal(boutdf[activity & day])
Ind_activity_bout_nodead_night_longitudinal = bout_length_longitudinal(boutdf[activity & night])




Ind_daily_locomotor_activity_data_nodead = sep_condition(locomotor_nodead).rename(columns = {"bout_length":"Activity"})
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