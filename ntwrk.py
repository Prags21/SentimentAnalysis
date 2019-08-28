import pandas as pd
import csv
table=pd.read_csv('Dataset.csv', delimiter = ',',encoding = "utf-8")
rt_list=['FiloSottile',
'gp_pulipaka' ,
'MikeQuindazzi',
'KirkDBorne',
'babadookspinoza',
'ACLU',
'Ronald_vanLoon',
'neptanum',
'Omkar_Raii',
'antgrasso',
'NicolaSturgeon',
'cindytrimm',
'ipfconline1',
'enricomolinari',
'Paula_Piccard',
'DrHassanRashidi',
'_timos_',
'Fabriziobustama',
'ValaAfshar',
'Jefferson_MFG',
'CadeMetz',
'evankirstel',
'Joshua4Congress',
'jose_garde',
'Fisher85M',
'SpirosMargaris',
'HeartIn_net',
'AndrewYang',
'rajat_shrimal',
'JeromeFosterII' ]
userList=[]
keys=['Screen Name','User Name','Tweet Created At','Tweet Text','User Location','Retweet Count','Phone Type','Hashtags']

def filter_users():
    for tweet in table.iterrows():
      count=0
      for item in rt_list:
        if(item in tweet[1]['Tweet Text']):
          count=count+1
      if(count>0):
          userList.append([tweet,count])

filter_users()
userList.sort(key=lambda x: x[1])
li=userList[-3500:]
with open('i_data.csv', 'a') as csvFile:
    dict_writer = csv.DictWriter(csvFile, fieldnames=keys)
    dict_writer.writeheader()
    for tweet in li:
        item=tweet[0][1]
        dict_ = {'Screen Name':item[0] ,
                 'User Name': item[1],
                 'Tweet Created At': item[2],
                 'Tweet Text': item[3],
                 'User Location': item[4],
                 'Retweet Count': item[5],
                 'Phone Type': item[6],
                 'Hashtags':item[7]
                }
        dict_writer.writerow(dict_)