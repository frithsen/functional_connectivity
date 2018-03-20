#!/usr/bin/env python3

import os
import numpy as np
import pandas as pd 
import scipy
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir('/tmp/mridata1/R01_Data_Func_Conn_Amy/SceneEncRet/results')

hemispheres = ['Left', 'Right']
conditions = ['study', 'test']


def clean_correlate_plot_data(age,mtl_region,colname):
    df = pd.concat([age,mtl_region],axis=1)  # make a new dataframe that contains just the two columns you want
    clean_df = df.dropna() # remove any rows that have NaNs
    no_outliers_df = clean_df[(np.abs(stats.zscore(clean_df)) < 3).all(axis=1)] # get rid of outliers if any (greater than 3* standard deviation)
    mtl_vals = scipy.stats.pearsonr(clean_df['age'],clean_df[colname]) # run the correlation (will spit out correlation coefficient and 2-tailed p-value)
    mtl_vals_no_outliers = scipy.stats.pearsonr(no_outliers_df['age'],no_outliers_df[colname]) # do the same as above but without the outliers
    sns.jointplot(x='age',y=colname,data=clean_df, kind="reg") # plot what it looks like WITH outliers
    plt.savefig(colname+'_'+hemisphere+'_'+condition+'.pdf') # save this
    sns.jointplot(x='age',y=colname,data=no_outliers_df, kind="reg") # plot what it looks like with the outliers removed
    plt.savefig(colname+'_'+hemisphere+'_'+condition+'_no_outliers.pdf') # save this

    return mtl_vals[0], mtl_vals[1], mtl_vals_no_outliers[0], mtl_vals_no_outliers[1]



for condition in conditions:
    for hemisphere in hemispheres:
        if condition == 'study' and hemisphere == 'Left':
            data = pd.read_csv('Left_study_results_all_subs.csv',header=0) # this is the file with all of the data (i.e., the fit values for each mtl region - for polynomial 1 and 2)
        elif condition == 'study' and hemisphere == 'Right':
            data = pd.read_csv('Right_study_results_all_subs.csv',header=0)
        elif condition == 'test' and hemisphere == 'Left':
            data = pd.read_csv('Left_test_results_all_subs.csv',header=0)
        elif condition == 'test' and hemisphere == 'Right':
            data = pd.read_csv('Right_test_results_all_subs.csv',header=0)


         # define the variables
        # --------------------------
        age = data.loc[:,['age']]
        alec_p1 = data.loc[:,['poly1_coef_alec']]
        alec_p2 = data.loc[:,['poly2_coef_alec']]
        pmec_p1 = data.loc[:,['poly1_coef_pmec']]
        pmec_p2 = data.loc[:,['poly2_coef_pmec']]
        tpole_p1 = data.loc[:,['poly1_coef_tpole']]
        tpole_p2 = data.loc[:,['poly2_coef_tpole']]
        prc_p1 = data.loc[:,['poly1_coef_prc']]
        prc_p2 = data.loc[:,['poly2_coef_prc']]
        rsc_p1 = data.loc[:,['poly1_coef_rsc']]
        rsc_p2 = data.loc[:,['poly2_coef_rsc']]
        phc_p1 = data.loc[:,['poly1_coef_phc']]
        phc_p2 = data.loc[:,['poly2_coef_phc']]

        
        [alec_poly1_coef, alec_poly1_p, alec_poly1_coef_noout, alec_poly1_p_noout]=clean_correlate_plot_data(age,alec_p1,'poly1_coef_alec')
        [alec_poly2_coef, alec_poly2_p, alec_poly2_coef_noout, alec_poly2_p_noout]=clean_correlate_plot_data(age,alec_p2,'poly2_coef_alec')
        [pmec_poly1_coef, pmec_poly1_p, pmec_poly1_coef_noout, pmec_poly1_p_noout]=clean_correlate_plot_data(age,pmec_p1,'poly1_coef_pmec')
        [pmec_poly2_coef, pmec_poly2_p, pmec_poly2_coef_noout, pmec_poly2_p_noout]=clean_correlate_plot_data(age,pmec_p2,'poly2_coef_pmec')
        [tpole_poly1_coef, tpole_poly1_p, tpole_poly1_coef_noout, tpole_poly1_p_noout]=clean_correlate_plot_data(age,tpole_p1,'poly1_coef_tpole')
        [tpole_poly2_coef, tpole_poly2_p, tpole_poly2_coef_noout, tpole_poly2_p_noout]=clean_correlate_plot_data(age,tpole_p2,'poly2_coef_tpole')
        [prc_poly1_coef, prc_poly1_p, prc_poly1_coef_noout, prc_poly1_p_noout]=clean_correlate_plot_data(age,prc_p1,'poly1_coef_prc')
        [prc_poly2_coef, prc_poly2_p, prc_poly2_coef_noout, prc_poly2_p_noout]=clean_correlate_plot_data(age,prc_p2,'poly2_coef_prc')
        [rsc_poly1_coef, rsc_poly1_p, rsc_poly1_coef_noout, rsc_poly1_p_noout]=clean_correlate_plot_data(age,rsc_p1,'poly1_coef_rsc')
        [rsc_poly2_coef, rsc_poly2_p, rsc_poly2_coef_noout, rsc_poly2_p_noout]=clean_correlate_plot_data(age,rsc_p2,'poly2_coef_rsc')
        [phc_poly1_coef, phc_poly1_p, phc_poly1_coef_noout, phc_poly1_p_noout]=clean_correlate_plot_data(age,phc_p1,'poly1_coef_phc')
        [phc_poly2_coef, phc_poly2_p, phc_poly2_coef_noout, phc_poly2_p_noout]=clean_correlate_plot_data(age,phc_p2,'poly2_coef_phc')


        corr_data = [alec_poly1_coef, alec_poly1_p, alec_poly2_coef, alec_poly2_p, pmec_poly1_coef, pmec_poly1_p, pmec_poly2_coef, pmec_poly2_p, tpole_poly1_coef, tpole_poly1_p, tpole_poly2_coef, tpole_poly2_p, prc_poly1_coef, prc_poly1_p, prc_poly2_coef, prc_poly2_p, rsc_poly1_coef, rsc_poly1_p, rsc_poly2_coef, rsc_poly2_p, phc_poly1_coef, phc_poly1_p, phc_poly2_coef, phc_poly2_p]
        corr_data = np.reshape(corr_data,(1,24))
        corr_data_df = pd.DataFrame(corr_data,columns=('alec_p1_coef', 'alec_p1_p', 'alec_p2_coef', 'alec_p2_p', 'pmec_p1_coef', 'pmec_p1_p', 'pmec_p2_coef', 'pmec_p2_p', 'tpole_p1_coef', 'tpole_p1_p', 'tpole_p2_coef', 'tpole_p2_p', 'prc_p1_coef', 'prc_p1_p', 'prc_p2_coef', 'prc_p2_p', 'rsc_p1_coef', 'rsc_p1_p', 'rsc_p2_coef', 'rsc_p2_p', 'phc_p1_coef', 'phc_p1_p', 'phc_p2_coef', 'phc_p2_p'))
        
        corr_data_noout = [alec_poly1_coef_noout, alec_poly1_p_noout, alec_poly2_coef_noout, alec_poly2_p_noout, pmec_poly1_coef_noout, pmec_poly1_p_noout, pmec_poly2_coef_noout, pmec_poly2_p_noout, tpole_poly1_coef_noout, tpole_poly1_p_noout, tpole_poly2_coef_noout, tpole_poly2_p_noout, prc_poly1_coef_noout, prc_poly1_p_noout, prc_poly2_coef_noout, prc_poly2_p_noout, rsc_poly1_coef_noout, rsc_poly1_p_noout, rsc_poly2_coef_noout, rsc_poly2_p_noout, phc_poly1_coef_noout, phc_poly1_p_noout, phc_poly2_coef_noout, phc_poly2_p_noout]
        corr_data_noout = np.reshape(corr_data_noout,(1,24))
        corr_data_noout_df = pd.DataFrame(corr_data_noout,columns=('alec_p1_coef', 'alec_p1_p', 'alec_p2_coef', 'alec_p2_p', 'pmec_p1_coef', 'pmec_p1_p', 'pmec_p2_coef', 'pmec_p2_p', 'tpole_p1_coef', 'tpole_p1_p', 'tpole_p2_coef', 'tpole_p2_p', 'prc_p1_coef', 'prc_p1_p', 'prc_p2_coef', 'prc_p2_p', 'rsc_p1_coef', 'rsc_p1_p', 'rsc_p2_coef', 'rsc_p2_p', 'phc_p1_coef', 'phc_p1_p', 'phc_p2_coef', 'phc_p2_p'))

        # save the output to a csv file
        if condition == 'study' and hemisphere == 'Left':
            corr_data_df.to_csv('Left_study_corr_all_subs.csv')
            corr_data_noout_df.to_csv('Left_study_corr_all_subs_noOutliers.csv')
        elif condition == 'study' and hemisphere == 'Right':
            corr_data_df.to_csv('Right_study_corr_all_subs.csv')
            corr_data_noout_df.to_csv('Right_study_corr_all_subs_noOutliers.csv')
        elif condition == 'test' and hemisphere == 'Left':
            corr_data_df.to_csv('Left_test_corr_all_subs.csv')
            corr_data_noout_df.to_csv('Left_test_corr_all_subs_noOutliers.csv')
        elif condition == 'test' and hemisphere == 'Right':
            corr_data_df.to_csv('Right_test_corr_all_subs.csv')
            corr_data_noout_df.to_csv('Right_test_corr_all_subs_noOutliers.csv')
