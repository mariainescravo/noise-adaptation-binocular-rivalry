# -*- coding: utf-8 -*-


''' --------- Imports ----------- '''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp
from prettytable import PrettyTable


''' --------- Pre-requisites: normality and variance ----------- '''


def normality(data_no_adap,data_div_adap,data_sub_adap):
    all_data = {'no_adap':data_no_adap,'div_adap':data_div_adap,'sub_adap':data_sub_adap}
    non_normal = []
    for metric in ['DomDur','MixDur','CV']:
        for noise in ['OU','Pink','White']:
            for adap in all_data.keys():
                data = all_data[adap]
                dist = data[noise+'_cs'][metric]
                p = sp.stats.shapiro(dist).pvalue
                if p < 0.05:
                    non_normal.append([metric,noise,adap])
    return non_normal

def equal_variance(data_no_adap,data_div_adap,data_sub_adap):
    all_data = {'no_adap':data_no_adap,'div_adap':data_div_adap,'sub_adap':data_sub_adap}
    non_equal_variance = []
    for metric in ['DomDur','MixDur','CV']:
        metric_data = []
        for noise in ['OU','Pink','White']:
            for adap in all_data.keys():
                data = all_data[adap]
                dist = data[noise+'_cs'][metric]
                metric_data.append(dist)
        p = sp.stats.levene(metric_data[0],metric_data[1],metric_data[2],
            metric_data[3],metric_data[4],metric_data[5]).pvalue
        if p < 0.05:
            non_equal_variance.append([metric])
    return non_equal_variance


''' --------- Multiple comparison ----------- '''

def build_each_df(noise,adap,data):
    df = pd.DataFrame({'noise': np.repeat([noise],len(data)),
        'adaptation': np.repeat([adap],len(data)),
        'metric': data})
    return df

def build_df_anova(data_no_adap,data_div_adap,data_sub_adap,metric):
    list_dfs = []
    for noise in ['OU','Pink','White']:
        no_adap  = data_no_adap[noise+'_cs'][metric]
        div_adap = data_div_adap[noise+'_cs'][metric]
        sub_adap = data_sub_adap[noise+'_cs'][metric]
        data = [no_adap,sub_adap,div_adap]
        for adap,d in zip(['no_adap','sub_adap','div_adap'],data):
            list_dfs.append(build_each_df(noise,adap,d))
    df = pd.concat(list_dfs)   
    return df


def comparison(metric,data_no_adap,data_div_adap,data_sub_adap):
    df = build_df_anova(data_no_adap,data_div_adap,data_sub_adap,metric)

    df['group'] = df['noise'].astype(str) +"_"+ df['adaptation'].astype(str)

    groups = df.group.unique()

    data = {g: pd.DataFrame() for g in groups}
    for key in data.keys():
        data[key] = df[:][df.group == key]


    table = PrettyTable(['Group 1','Group 2','Mann-Whitney p','Reject'],float_format='.10')

    for i in range(0,9):
        for j in range(i+1,9):
            u,p1 = sp.stats.mannwhitneyu(data[groups[i]]['metric'],data[groups[j]]['metric'])
            table.add_row([groups[i],groups[j],p1*36,p1*36<0.05])
    return table

