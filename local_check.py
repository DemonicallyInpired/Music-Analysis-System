import re
import os
import sys
from termcolor import colored, cprint
import numpy as np
from tabulate import tabulate
import pandas as pd
import os
Error_log = open("Output/ffmpeg.txt", "r")
Media_log = open("Output/mediainfo.txt", "r")
log_list = [lines.rstrip("\n") for lines in Error_log]
def processErrorlist():
    count = 0
    for i in range(1, len(log_list), 2):
        if(i < len(log_list) and log_list[i]!= ""):
            count = i
            while(log_list[count] != "" and count != len(log_list)-1):
                if(count == i):
                    count += 1
                else:
                    log_list[i] += str(" "+log_list[count])
                    count += 1
    for i in range(0, len(log_list)-3):
        if(log_list[i] !="" and log_list[i+1] != "" and log_list[i+2] != ""):
            del log_list[i+2]
    for i in range(0, len(log_list)-1, 2):
        if(log_list[i] == ""):
            del log_list[i]
    #print(offset, count)
    #del log_list[offset: count-1]
    return log_list
log_list = processErrorlist()   
names = [log_list[i] for i in range(0, len(log_list)-1) if i%2 == 0]
errors = [log_list[i] for i in range(len(log_list)) if i % 2 == 1]
log_dict = []
for i in range(len(names)):
    if(len(errors[i])>0):
        log_dict.append({"name": names[i], "error": errors[i], "Video":False})
    else:
        log_dict.append({"name": names[i], "error": errors[i], "Video":False})

Media_list = pd.Series(Media_log.readlines())
audio_index = list(Media_list[Media_list=='Audio\n'].index)
video_index = list(Media_list[Media_list=='Video\n'].index)
print("*************")
print(video_index, audio_index)

def findnext_index_lower(audio_index, video_index):
    for i in audio_index:
        for j in video_index:
            if(len(video_index) > 0 and (j<i)):
                return audio_index.index(i)
            else:
                pass    
def CheckVideo():    
    if(findnext_index_lower(audio_index, video_index) == None):
          pass
    else:
        log_dict[findnext_index_lower(audio_index, video_index)]["Video"] = True
CheckVideo()

print(log_dict)

videos = [log_dict[j]['Video'] for j in range(len(log_dict))]
final_log_table = pd.DataFrame(columns = ['Name', 'Error'])
final_log_table['Name'] = names
final_log_table['Error'] = errors
final_log_table['Video'] = videos
print(final_log_table)

verified_files = []
def return_verified():

    for i in range(len(log_dict)):
        if(len(log_dict[i]['error']) > 0 or log_dict[i]["Video"] == True):
            print(colored("Found errors in the file{}\n Deleting the unsupported files and curroupted files ...",'red', attrs=['reverse', 'blink']).format(names[i]))
            os.remove("data/"+names[i])
        if(log_dict[i]['error'] == '' and log_dict[i]['Video'] == False): 
            verified_files.append(log_dict[i]["name"])
    print(verified_files)
    return verified_files
return_verified()