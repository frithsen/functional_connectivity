#!/bin/bash
#$ -S /bin/bash -V
#$ -j y
#$ -pe openmp 4
#$ -l dh=1
#$ -o /tmp/mridata4/NIA_R01_MRI_Data/SceneEncRet_fMRI/gridlog
#$ -q stark.q,shared.q
#$ -cwd


# Log some useful stuff into that log file
echo Started at `date` in `pwd`
if [ -n "$HOST" ]
then
        echo Host is $HOST
fi
if [ -n "$HOSTNAME" ]
then
        echo Hostname is $HOSTNAME
fi
if [ ! -n "$NSLOTS" ]; then
NSLOTS=1
fi

echo Using $NSLOTS slots
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=$NSLOTS
export OMP_NUM_THREADS=$NSLOTS

# Use the latest version of ANTS
export ANTSPATH=`/tmp/mribin/mri/GetLatestANTSPath`
echo "Using ANTS from $ANTSPATH"

# Enter Ss directory - the "cwd" flag in qsub lets us be relative, assuming we're in the
#  main study directory.  This lets us call the script with either a relative directory
#  name (e.g., "qsub myanalysis.sh 123456") or with the full directory (e.g.,
#  "qsub myanalysis.sh /tmp/mridata1/mystudy/123456")
# Alternatively, the "cd $1" can be "cd /tmp/mridataX/mystudy/$1" to ensure you get there.
cd $1
echo Running on subject $1 in `pwd`
# Let the output log file know where I am



# ---------- create stricter motion censor files (use .5 degrees and .5 mm as the threshold) -------
/tmp/mribin/mri/move_censor.pl -mm_thresh 0.5 -deg_thresh 0.5 -file motion_study1 -file motion_study2 -file motion_study3 -file motion_study4
mv motion_censor_vector.txt motion_censor_vector_verystrict_study.txt


# ------------- If subject hasn't been Freesurfer-ed, let me know, send it to the grid to get Freesurfer'ed, and exit --------------
if [ ! -e freesurfer/mri ]; then
    echo "Need to Freesurfer subject"
    cd ../
    qsub /tmp/mribin/mri/FS_Single_Subject.sh $1
    echo "Sent off to grid"
    exit
fi


# Create stricter masks 

 3dTstat -mean -prefix MEAN_study run_allruns_study+orig.
 3dAutomask -prefix MEAN_study_mask MEAN_study+orig.

 3dTstat -mean -prefix MEAN_test run_allruns_test+orig.
 3dAutomask -prefix MEAN_test_mask MEAN_test+orig.



# ------------ check how much motion there is ---------------------- #
 /tmp/mribin/mri/check_motion_file.bash motion_censor_vector_verystrict_study.txt study 90 # this will output a file called 'good_motion_sub_study' if there isn't too much motion


# ------------------- STUDY SESSION ---------------------------------

if [ -e good_motion_sub_study ]; then  # if that file exists, carry on

# -------------- Normalize BOLD data ---------------------- divide each voxel by its mean and multiply by 100 to get something akin to % signal change
    
# Get the mean voxel intensity of each run
         for j in `count -d 1 1 4`; do
         3dTstat -prefix mean_run_study${j}_AF -mask MEAN_study_mask+orig. run_study${j}+orig.
         done

    # #  Divide each voxel by the mean and scale it by 100
	#     # a/b*100 is the base expression - divide each value by the mean for the given run, then multiply by 100 (the new mean is 100)
	#     # min(200) is used to make sure there are no large scaled values (usually occurring outside of the brain). min will take the minimum of either 200 or the result of the math
	#     # step(a) means to truncate negative values to zero (usually happens from a mask, blur, or warping operation)
	#     # step(b) means to truncate negative mean values to zero

         for j in `count -d 1 1 4`; do
         3dcalc -a run_study${j}+orig. -b mean_run_study${j}_AF+orig. -expr 'min(200, a/b*100)*step(a)*step(b)' -prefix scaled_run_study${j}_AF
         done

# -------------- ANATICOR data (get rid of signal from WM & CSF) --------------------
    
    for j in `count -d 1 1 4`; do
    ln -s motion_study${j} motion_study${j}.1D
    @ANATICOR -ts scaled_run_study${j}_AF+orig -motion motion_study${j}.1D -polort 3 -aseg freesurfer/mri/aseg.nii -prefix scaled_run_study${j}_AC
    done

# ------------- Calculate the global signal (will be used for later regression) -------------
    for j in `count -d 1 1 4`; do
    3dmaskave -quiet -mask MEAN_study_mask.nii scaled_run_study${j}_AF+orig > global_sig_study${j}.1D
    done

# ------------- Combine the anaticor'ed runs, the global signal and the motion parameters across runs (needed for regression in next step) ---------------
    3dTcat -prefix scaled_study_allruns_AC scaled_run_study?_AC+orig.HEAD #scaled_run_study1_AC+orig scaled_run_study1_AC+orig scaled_run_study1_AC+orig
    cat global_sig_study?.1D > global_sig_study_allruns
    cat motion_study? > motion_study_allruns

# -------------- Run Regression, censor, and bandpass results (3dTproject is arguably better for fc than 3dDeconvolve) ----------------
    ln -s motion_study_allruns motion_study_allruns.1D  # make a symbolic link to make AFNI happy
    ln -s global_sig_study_allruns global_sig_study_allruns.1D

    3dTproject \
    -input scaled_study_allruns_AC+orig \
    -prefix scaled_study_allruns_AC_regression \
    -censor motion_censor_vector_verystrict_study.txt \
    -cenmode KILL \
    -concat '1D: 0 104 208 312' \
    -ort motion_study_allruns.1D \
    -ort global_sig_study_allruns.1D \
    -polort 0 \
    -passband .009 .08 \
     -mask MEAN_study_mask.nii


else
    echo "bad motion sub, skipping study session"
fi
