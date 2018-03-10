#!/usr/bin/env python3

import os
import glob
import numpy as np


hippo_regions = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']
hemispheres = ['Left', 'Right']
mtl_regions = ['alEC', 'pmEC', 'Tpole', 'PRC', 'RSC', 'PHC']
conditions = ['study', 'test']

# Find subjects
subjects = glob.glob('/path_to_your_data/??-??/12????')
dir_path = '/tmp/mridata4/NIA_R01_MRI_Data/SceneEncRet_fMRI'

Left_Corr_vals_study = np.zeros(36)
Right_Corr_vals_study = np.zeros(36)
Left_Corr_vals_test = np.zeros(36)
Right_Corr_vals_test = np.zeros(36)


Left_Corr_vals_fisher_study = np.zeros(36)
Right_Corr_vals_fisher_study = np.zeros(36)
Left_Corr_vals_fisher_test = np.zeros(36)
Right_Corr_vals_fisher_test = np.zeros(36)

def do_hemispheres():
    print(subject+' '+hemisphere+' '+condition+' '+hippo_region+' '+mtl_region) # tell me what you are working on
    hippo_ts = os.path.join(subject,'timeseries',hemisphere+'_Hippo_'+hippo_region+'_'+condition+'_timeseries.1D')  # this file has the timeseries data in a single column
    data2 = np.loadtxt(hippo_ts) # create a variable named 'data1' and store the timeseries data in it
    hippo_check = os.path.join(subject,'Percent_Zero',hemisphere+'_Hippo_'+hippo_region+'_'+condition+'.txt')  # this file contains a 1 if the data is good and a 0 if the data is bad (data could be bad due to poor coverage of the ROI)
    f = open(hippo_check, "r+")
    hippo_check = int(f.read())
    f.close()
    if hippo_check == 1: # if the hippo_region timeseries data is good, do the correlation and return the correlation coefficient
        corr_val = np.corrcoef(data1,data2)
        corr_coef = corr_val[1,0]
        corr_coef_fisher = np.arctanh(corr_coef)
    elif hippo_check == 0:  # if it's bad, return a NaN and tell me
        corr_coef = np.NAN
        corr_coef_fisher = np.NAN
        print ('Bad MTL ROI ' + hemisphere + ' ' + mtl_region + ' ' + hippo_region + ' ' + condition)
    return corr_coef,corr_coef_fisher   


for subject in subjects:
    i = 0
    j = 0
    k = 0
    l = 0
    sub_ID = subject[-12:]
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
                    data1 = np.loadtxt(mtl_ts) # create a variable called 'data2' and store the timeseries data in it
                    mtl_check = os.path.join(subject,'Percent_Zero',hem+'_'+mtl_region+'_'+condition+'.txt') # this will signify if the data is good (1) or bad (0)
                    f2 = open(mtl_check, "r+") # open the file 
                    mtl_check = int(f2.read()) # read it
                    f2.close() # close the file
                    if mtl_check == 1: # if the mtl timeseries data is good, continue
                        for hippo_region in hippo_regions: 
                            if hemisphere == 'Left':
                                if condition == 'study':
                                    [Left_Corr_vals_study[i],Left_Corr_vals_fisher_study[i]]=do_hemispheres()
                                    i+=1
                                elif condition == 'test':
                                    [Left_Corr_vals_test[j],Left_Corr_vals_fisher_test[j]]=do_hemispheres()
                                    j+=1                              
                            elif hemisphere == 'Right':
                                if condition == 'study':
                                    [Right_Corr_vals_study[k],Right_Corr_vals_fisher_study[k]]=do_hemispheres()
                                    k+=1
                                elif condition == 'test':
                                    [Right_Corr_vals_test[l],Right_Corr_vals_fisher_test[l]]=do_hemispheres()
                                    l+=1
                    elif mtl_check == 0:
                            print ('Bad Hippo ROI ' + hemisphere + ' ' + hippo_region + ' ' + condition)  # this means that the hippocampus timeseries datafile has been flagged as bad due to poor coverage. if this is the case, let me know and mark the next 6 rows of the output file with NaNs
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





