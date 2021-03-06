#!/usr/bin/env python3

import os
import glob
import numpy as np


hippo_regions = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6'] # the hippocampus regions you are looking at
hemispheres = ['Left', 'Right'] # which hemispheres
mtl_regions = ['alEC', 'pmEC', 'Tpole', 'PRC', 'RSC', 'PHC'] # what specific MTL cortical areas you want
conditions = ['study', 'test'] # the specific testing conditions

# Find subjects
subjects = glob.glob('/path_to_your_data/??-??/12????') # state the path to where your data lives
dir_path = 'path_to_top_directory_of_where_data_lives'

num_data_points = len(hippo_regions) * len(mtl_regions)

Left_Corr_vals_study = np.zeros(num_data_points) 
Right_Corr_vals_study = np.zeros(num_data_points)
Left_Corr_vals_test = np.zeros(num_data_points)
Right_Corr_vals_test = np.zeros(num_data_points)


Left_Corr_vals_fisher_study = np.zeros(num_data_points)
Right_Corr_vals_fisher_study = np.zeros(num_data_points)
Left_Corr_vals_fisher_test = np.zeros(num_data_points)
Right_Corr_vals_fisher_test = np.zeros(num_data_points)

def run_correlation():
    print(subject+' '+hemisphere+' '+condition+' '+hippo_region+' '+mtl_region) # echo to the screen the specifics of what is being done
    hippo_ts = os.path.join(subject,'timeseries',hemisphere+'_Hippo_'+hippo_region+'_'+condition+'_timeseries.1D')  # this file has the timeseries data in a single column
    data2 = np.loadtxt(hippo_ts) # create a variable named 'data2' and store the timeseries data in it
    hippo_check_file = os.path.join(subject,'Percent_Zero',hemisphere+'_Hippo_'+hippo_region+'_'+condition+'.txt')  # this file contains a 1 if the data is good and a 0 if the data is bad (data could be bad due to poor coverage of the ROI)
    f = np.loadtxt(hippo_check_file)
    if hippo_check == 1: # if the hippo_region timeseries data is good, do the correlation and return the correlation coefficient
        corr_val = np.corrcoef(data1,data2) # correlate 
        corr_coef = corr_val[1,0]
        corr_coef_fisher = np.arctanh(corr_coef) # fisher transform coefficient 
    elif hippo_check == 0:  # if it's bad, return a NaN and tell me
        corr_coef = np.NAN
        corr_coef_fisher = np.NAN
        print ('Bad Hippo ROI '+ hippo_region + '_' +hemisphere)
    return corr_coef,corr_coef_fisher   


for subject in subjects:
    i = 0
    j = 0
    k = 0
    l = 0
    sub_ID = subject[-12:] # only grab the last 12 characters of the subject path (this is the subject identifier)
    print (sub_ID)
    for hemisphere in hemispheres:
        hem= hemisphere[0]
        for condition in conditions:
            if condition == 'study':
                good_subject_check = os.path.join(dir_path,sub_ID,'good_motion_sub_study')
            elif condition == 'test':
                good_subject_check = os.path.join(dir_path,sub_ID,'good_motion_sub_test')
            if os.path.isfile(good_subject_check): # if it's a 'good' subject, then continue
                for mtl_region in mtl_regions:
                    mtl_ts = os.path.join(subject,'timeseries',hem+'_'+mtl_region+'_'+condition+'_timeseries.1D') # this is the mtl region timeseries data
                    data1 = np.loadtxt(mtl_ts) # create a variable called 'data1' and store the timeseries data in it
                    mtl_check_file = os.path.join(subject,'Percent_Zero',hem+'_'+mtl_region+'_'+condition+'.txt') # this will signify if the data is good (1) or bad (0)
                    mtl_check = np.loadtxt(mtl_check_file)
                    if mtl_check == 1: # if the mtl timeseries data is good, continue
                        for hippo_region in hippo_regions: 
                            if hemisphere == 'Left':
                                if condition == 'study':
                                    [Left_Corr_vals_study[i],Left_Corr_vals_fisher_study[i]]=run_correlation()
                                    i+=1
                                elif condition == 'test':
                                    [Left_Corr_vals_test[j],Left_Corr_vals_fisher_test[j]]=run_correlation()
                                    j+=1                              
                            elif hemisphere == 'Right':
                                if condition == 'study':
                                    [Right_Corr_vals_study[k],Right_Corr_vals_fisher_study[k]]=run_correlation()
                                    k+=1
                                elif condition == 'test':
                                    [Right_Corr_vals_test[l],Right_Corr_vals_fisher_test[l]]=run_correlation()
                                    l+=1
                    elif mtl_check == 0:
                            print ('Bad MTL ROI ' + hemisphere + ' ' + mtl_region ) # this means that the mtl timeseries datafile has been flagged as bad due to poor coverage. if this is the case, let me know and mark the next 6 rows of the output file with NaNs
                            if hemisphere == 'Left' and condition == 'study':
                                Left_Corr_vals_study[i:i+6] = np.NAN
                                Left_Corr_vals_fisher_study[i:i+6] = np.NAN
                                i+=6
                            elif hemisphere == 'Left' and condition == 'test':
                                Left_Corr_vals_test[j:j+6] = np.NAN
                                Left_Corr_vals_fisher_test[j:j+6] = np.NAN
                                j+=6
                            elif hemisphere == 'Right' and condition == 'study':
                                Right_Corr_vals_study[k:k+6] = np.NAN
                                Right_Corr_vals_fisher_study[k:k+6] = np.NAN
                                k+=6
                            elif hemisphere == 'Right' and condition == 'test':
                                Right_Corr_vals_test[l:l+6] = np.NAN
                                Right_Corr_vals_fisher_test[l:l+6] = np.NAN
                                l+=6
                            else:
                                print ('something went wrong')
                    else:
                        print ('Do not know if mtl timeseries data is good or bad')


    # now to save the data
    #-----------------------------
    os.chdir(subject)  # go to the subject's directory
        
    good_study_sub = os.path.join(dir_path,sub_ID,'good_motion_sub_study')
    bad_study_sub = os.path.join(dir_path,sub_ID,'bad_motion_sub_study')

    if os.path.isfile(good_study_sub):  # check if this is a 'good' subject (could be bad due to subject moving too much, falling asleep, etc.), if it is, then save the file created
        np.savetxt('L_corr_vals_study.txt', Left_Corr_vals_study, fmt='%1.3f')
        np.savetxt('R_corr_vals_study.txt', Right_Corr_vals_study, fmt='%1.3f')
        np.savetxt('L_corr_vals_fisher_study.txt', Left_Corr_vals_fisher_study, fmt='%1.3f')
        np.savetxt('R_corr_vals_fisher_study.txt', Right_Corr_vals_fisher_study, fmt='%1.3f')
        print('Study Data Saved')
    elif os.path.isfile(bad_study_sub):  # if it's a bad subject, let me know and move on to the next
        print ('Bad Study Subject')
    else: 
        print ('Do not know if study sessions are good or bad')  # this means that the good/bad file cannot be found (has it been created?)
        
    good_test_sub = os.path.join(dir_path,sub_ID,'good_motion_sub_test')
    bad_test_sub = os.path.join(dir_path,sub_ID,'bad_motion_sub_test')

    if os.path.isfile(good_test_sub):
        np.savetxt('L_corr_vals_test.txt', Left_Corr_vals_test, fmt='%1.3f')
        np.savetxt('R_corr_vals_test.txt', Right_Corr_vals_test, fmt='%1.3f')
        np.savetxt('L_corr_vals_fisher_test.txt', Left_Corr_vals_fisher_test, fmt='%1.3f')
        np.savetxt('R_corr_vals_fisher_test.txt', Right_Corr_vals_fisher_test, fmt='%1.3f')
        print('Test Data Saved')    
    elif os.path.isfile(bad_test_sub):
        print ('Bad Test Subject')
    else:
        print ('Do not know if test sessions are good or bad')





