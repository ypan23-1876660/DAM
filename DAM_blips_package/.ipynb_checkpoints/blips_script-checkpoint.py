#!/usr/bin/env python
# coding: utf-8

import getopt, sys
import pandas as pd
import os
import re
import numpy as np
from datetime import datetime, date, timedelta


#Read in user variables
argv = sys.argv[1:]
output_file_path = None

try:
    opts, args = getopt.getopt(argv, "s:e:")
    
except:
    print("Error")
        
for opt, arg in opts:
    if opt in ['-s']:
        sdate = str(arg)
    elif opt in ['-e']:
        edate = str(arg)



#Set to working directory
cwd = os.getcwd()
os.chdir(str(cwd) + "/data")


#Select exp dates
def select_dates(df, start_date, end_date):
    #Filter start and end date
    start_date = (df['Date'] == sdate) & (df['Time'] == "00:00:00") 
    end_date = (df['Date'] == edate) & (df['Time'] == "23:59:00")

    #Get the indices of start and end date
    start_date_index = int(df[start_date]['Index']-1)
    end_date_index = int(df[end_date]['Index']-1)

    #Filter file based on selected dates & reset index of the new selected dataframe
    df1 = df.loc[start_date_index:end_date_index].reset_index(drop=True)
    return(df1)


#Find blips based on the last two characters are not equal to "00"
def find_blips(df):
    blips = []
    for i in range(len(df)):
        last_char = df['Time'].iloc[i][-2:]
        if last_char != "00":
            blips.append(i)
    df_blips = df.iloc[blips,:]
    return (df_blips)


#Find where the blips are in the original df and fix all to "00"
def fix_blips(df, blips):

    #Convert index.series to integer
    int_index = list(blips.index)
    for i in int_index:
        i = int(i)

    #Fix the blips
    for i in df.index:
        for a in int_index:
            if i == a:
                split_time = df.loc[i]['Time'].split(":")
                hour = split_time[0] 
                minute = split_time[1]
                sec = "00"
                new_time = hour + ":" + minute + ":" + sec
                df.loc[i, 'Time'] = new_time
    print(df.loc[int_index])
    return(df)
    


def fix_blips2(df):
    #Create a new column with datetime
    df['date_time'] = df['Date'] + ' ' + df['Time']
    df['date_time'] = pd.to_datetime(df['date_time'])
    
    #Calculate Experimental days for checking if nrow = template row 

    s= datetime.strptime(sdate, '%d %b %y')
    e = datetime.strptime(edate, '%d %b %y')
    exp_days = (e-s).days+1
    
    #Create time template 
    date_times = pd.date_range(start = sdate + ' ' + '00:00:00', end = edate + ' ' + '23:59:00', freq = 'min')
    date_times = pd.DataFrame(date_times).rename(columns={0:'date_time'})
    date_times['Date'] = date_times['date_time'].dt.strftime("%-d %b %y")
    date_times['Time'] = date_times['date_time'].dt.strftime("%H:%M:%S")
    template = date_times[['Date', 'Time']]
    
    #Hardcode if the first and last column is missing. If so, insert first and last row
    if df.loc[0 , 'Time'] != '00:00:00':
        df = df.append(date_times.loc[0], ignore_index=False).sort_values('date_time').reset_index(drop=True)
        df.bfill(inplace=True)
    if df.iloc[-1]['Time'] != '23:59:00':
        df = df.append(date_times.iloc[-1], ignore_index=False).sort_values('date_time').reset_index(drop=True)
        df.ffill(inplace=True)
        
    #Calculate the time difference
    df['time_diff'] = df['date_time'].diff()  #Find the difference between two rows for the whole dataframe
    df['time_diff'] = round(df['time_diff'].dt.total_seconds()/60, 3) 
    
    #Check if first and last rows are inserted and change time_diff is 1
    if df.loc[0, 'Time'] == '00:00:00':
        df.loc[0, 'time_diff'] = 1
    if df.iloc[-1]['Time'] == '23:59:00':
        df.loc[df.index[-1], "time_diff"] = 1
    
    #Find the time difference that does not equal to 1. Return the list of indices where of where the gaps are, and convert indices to int
    gap = df.loc[df['time_diff'] != 1]
    gap_index = list(gap.index)
    for i in gap_index:
        i = int(i)
    
    print(str(raw) + ' Gaps')
    print(gap)
    #Find the missing rows from the template
    new_index_list= []
    for i in gap_index:
        new_index = list(range(i, (int(df.loc[i, 'time_diff'] -2 +i))+1))
        new_index_list.extend(new_index)
    
    #Insert missing rows at correct position and fill in nan value with previous row value 
    df = df.append(date_times.loc[new_index_list], ignore_index=False).sort_values('date_time').reset_index(drop=True)
    df.ffill(inplace=True)
    
    print(str(raw) + ' Corrected_Gaps')
    print(df.loc[gap_index])
        
    df['Date'].replace(template['Date'], inplace=True)
    df['Time'].replace(template['Time'], inplace=True)
    df = df.drop(['date_time', 'time_diff'], axis=1)
    
    #Check if df nrow == template nrow, if so, overlay template time with df time
    if ((exp_days)*1440 == len(df.index)) != True:
        print(df[(df['date_time'] == date_times['date_time']) == False])
    
    return(df)

   
#Loop through all the monitors and save each txt to output_txt
for raw in os.listdir((str(cwd) + '/data')):
    if raw.endswith(".txt"):
        file = pd.read_csv(raw, delimiter = "\t", header=None)
        file = file.rename(columns={file.columns[0]: 'Index', file.columns[1]: 'Date', file.columns[2]: 'Time'})
        
        df = select_dates(file, sdate, edate)
        
        print(str(raw) + ' Blips')
        blips = find_blips(df)
        print(blips)
        
        print(str(raw) + ' Corrected_blips')
        fixed1 = fix_blips(df, blips)
        
        fixed2 = fix_blips2(fixed1)
        
        print(str(raw) + ' Preview of the first 5 rows of the output txt file')
        print(fixed2.head(5))
        
        print(str(raw) + ' Preview of the last 5 rows of the output txt file')
        print(fixed2.tail(5))
        
        np.savetxt((str(cwd) + '/output/output_txt/' + 'adj_' + str(raw)), fixed2.values, fmt='%s')
     