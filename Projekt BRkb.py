# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 20:40:11 2022

@author: Karol
"""

import pandas as pd
import numpy as np
import regex
import datetime

br_active= pd.read_csv('active boxers/results_grandtotal_active.csv')

br_active_cleaned= br_active.drop(columns=['KOs','rounds'])
br_active_cleaned[['height inch', 'height cm']]= br_active_cleaned['height'].str.split(' / ', 1, expand=True)
br_active_cleaned[['reach inch', 'reach cm']]= br_active_cleaned['reach'].str.split(' / ', 1, expand=True)
br_active_cleaned[['rating_world_position', 'rating_world_category']]= br_active_cleaned['rating_word'].str.split(' / ', 1, expand=True).replace(',','', regex=True)
br_active_cleaned[['rating_native_position', 'rating_native_category']]= br_active_cleaned['rating_native'].str.split(' / ', 1, expand=True).replace(',','', regex=True)
br_active_cleaned[['career start', 'career edge']]= br_active_cleaned['career'].str.split('-', 1, expand=True)
br_active_cleaned['reach cm']= br_active_cleaned['reach cm'].str.extract(r'([0-9]+)')
br_active_cleaned['height cm']= br_active_cleaned['height cm'].str.extract(r'([0-9]+)')
br_active_cleaned['wins_by_KO']= br_active_cleaned['wins_by_KO'].str.extract(r'([0-9]+)')
br_active_cleaned['defeats_by_KO']= br_active_cleaned['defeats_by_KO'].str.extract(r'([0-9]+)')


br_active_cleaned = br_active_cleaned.astype({'rating_world_position':'float',
                                              'rating_native_position':'float',
                                              'reach cm':'float',
                                              'height cm':'float',
                                              'wins':'float',
                                              'defeats':'float',
                                              'draws':'float',
                                              'bouts':'float',
                                              'wins_by_KO':'float',
                                              'defeats_by_KO':'float',
                                              'age':'float',
                                              'points':'float'})

br_active_cleaned['KOWratio'] = (br_active_cleaned['wins_by_KO']/br_active_cleaned['bouts']).round(4).fillna(0)
br_active_cleaned['KOWPratio'] = (br_active_cleaned['wins_by_KO']/br_active_cleaned['wins']).round(4).fillna(0)
br_active_cleaned['KODratio'] = (br_active_cleaned['defeats_by_KO']/br_active_cleaned['bouts']).round(4).fillna(0)
br_active_cleaned['KODPratio'] = (br_active_cleaned['defeats_by_KO']/br_active_cleaned['defeats']).round(4).fillna(0)

#przekodowywanie ostanich 6 walk na wektor

def lastone (i):
    if (i=="W"):
        return 6
    elif (i=="D"):
        return 5
    elif (i=="L"):
        return 3
    elif (i=='NC'):
        return 1
    elif (i=='B'):
        return 0
    else:
        return "nan"
    

br_active_cleaned['last1V']= [lastone(i) for i in br_active_cleaned[['last1']].values] 
   
 #przekodowywanie ostanich 6 walk na wektor
def lasttwo (i):
    if (i=="W"):
        return 5
    elif (i=="D"):
        return 4
    elif (i=="L"):
        return 2
    elif (i=='NC'):
        return 1
    elif (i=='B'):
        return 0
    else:
        return "nan"    

br_active_cleaned['last2V']= [lasttwo(i) for i in br_active_cleaned[['last2']].values]     

 #przekodowywanie ostanich 6 walk na wektor
def lastthree (i):
    if (i=="W"):
        return 4
    elif (i=="D"):
        return 3
    elif (i=="L"):
        return 1
    elif (i=='NC'):
        return 0
    elif (i=='B'):
        return 0
    else:
        return "nan"    

br_active_cleaned['last3V']= [lastthree(i) for i in br_active_cleaned[['last3']].values] 

 #przekodowywanie ostanich 6 walk na wektor
def lastfour (i):
    if (i=="W"):
        return 3
    elif (i=="D"):
        return 2
    elif (i=="L"):
        return 0
    elif (i=='NC'):
        return 0
    elif (i=='B'):
        return 0
    else:
        return "nan"    

br_active_cleaned['last4V']= [lastfour(i) for i in br_active_cleaned[['last4']].values] 

 #przekodowywanie ostanich 6 walk na wektor
def lastfive (i):
    if (i=="W"):
        return 2
    elif (i=="D"):
        return 0
    elif (i=="L"):
        return -1
    elif (i=='NC'):
        return 0
    elif (i=='B'):
        return 0
    else:
        return "nan"    

br_active_cleaned['last5V']= [lastfive(i) for i in br_active_cleaned[['last5']].values]

 #przekodowywanie ostanich 6 walk na wektor
def lastsix (i):
    if (i=="W"):
        return 1
    elif (i=="D"):
        return 0
    elif (i=="L"):
        return -2
    elif (i=='NC'):
        return 0
    elif (i=='B'):
        return 0
    else:
        return "nan"    

br_active_cleaned['last6V']= ([lastsix(i) for i in br_active_cleaned[['last6']].values])

br_active_cleaned['last6Fwec']= br_active_cleaned['last1V']+br_active_cleaned['last2V']+br_active_cleaned['last3V']+br_active_cleaned['last4V']+br_active_cleaned['last5V']+br_active_cleaned['last6V']

br_active_cleaned['debut'] = pd.to_datetime(br_active_cleaned['debut'])

br_active_cleaned['career_period'] = (pd.to_datetime(br_active_cleaned['debut'])-pd.to_datetime(br_active_cleaned['career edge'])).abs().dt.days

work_atributes = ['boxerID','age','wins', 'defeats', 'draws', 'wins_by_KO', 'defeats_by_KO',
 'division', 'bouts','debut','career start','career edge',
 'nationality', 'stance', 'MMA', 'boxer','height cm','reach cm',
 'points','rating_world_position','rating_world_category', 'rating_native_position','rating_native_category',
 'last1', 'last2','last3', 'last4', 'last5', 'last6','titles.held',
 'KOWratio','KOWPratio','KODratio','KODPratio','last6Fwec']

br_active_work= br_active_cleaned.loc[:,work_atributes]

a= br_active_work[br_active_cleaned['rating_world_position'].isna()]

br_active.head()

br_active_cleaned_mmaf = br_active_cleaned.dropna(subset=['MMA'])
br_active_cleaned_mman = br_active_cleaned[br_active_cleaned['MMA'].isnull()]
br_active_cleaned_mman=br_active_cleaned_mman.assign(MMA='N')
br_active_cleaned_mmaf=br_active_cleaned_mmaf.assign(MMA='Y')
br_active_cleaned= pd.concat([br_active_cleaned_mmaf,br_active_cleaned_mman], axis=0)

# Tworzę tabelę do analizy 
# wybieram kolumny z ktorych bede chcial skorzystać
work_atributes = ['boxerID','age','wins', 'defeats', 'draws', 'wins_by_KO', 'defeats_by_KO',
 'division', 'bouts','debut','career edge','career_period',
 'nationality', 'stance', 'MMA', 'boxer','height cm','reach cm',
 'points','rating_world_position','rating_world_category', 'rating_native_position','rating_native_category',
 'last1', 'last2','last3', 'last4', 'last5', 'last6','titles.held',
 'KOWratio','KOWPratio','KODratio','KODPratio','last6Fwec']

# Tworzę nowy DF do analizy
br_active_work= br_active_cleaned.loc[:,work_atributes]
braw = br_active_work.copy()
# wyrzucam kolumny z najwiekszymi brakami danych
braw= braw.drop(columns= ['titles.held','reach cm','height cm','stance'])
# wyrzucam braki w danych 
braw= braw.dropna()



braw.isna().sum().sort_values(ascending=True)


#usuwam dane powyżej 99 percentylu
braw[braw.age < np.percentile(braw.age,99)]
braw[braw.wins < np.percentile(braw.wins,99)]
braw[braw.defeats < np.percentile(braw.defeats,99)]
braw[braw.draws < np.percentile(braw.draws,99)]
braw[braw.wins_by_KO < np.percentile(braw.wins_by_KO,99)]
braw[braw.defeats_by_KO < np.percentile(braw.defeats_by_KO,99)]
braw[braw.bouts < np.percentile(braw.bouts,99)]
braw[braw.points < np.percentile(braw.points,99)]
braw[braw.rating_world_position < np.percentile(braw.rating_world_position,99)]
braw[braw.rating_native_position < np.percentile(braw.rating_native_position,99)]
braw[braw.KODPratio < np.percentile(braw.KODPratio,99)]
braw[braw.KOWPratio < np.percentile(braw.KODPratio,99)]
braw[braw.KOWratio < np.percentile(braw.KODPratio,99)]
braw[braw.KODratio < np.percentile(braw.KODPratio,99)]
braw[braw.last6Fwec < np.percentile(braw.last6Fwec,99)]


a = braw.loc[:,['boxerID','division']].groupby(['division']).count().reset_index()
