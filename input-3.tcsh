## THIS FILE FORMAT IS SUBJECT TO CHANGE. THINK OF IT AS A PLACEHOLDER

# LAB: This is a fancy test
# KW: dti, fast, python
# ENV
set myenv = ( 3 58 )
setenv OMP_NUM_THREADS ( 1 4 )
# INP
set param_stat  = ( -mean -sd -median )
set indir = ( AFNI_demos/FATCAT_DEMO )
# CMD
3dBRIKSTAT                                                                          \
    -stat ${param_stat[1]}                                                          \
    -prefix {outfile}.nii.gz                                                        \
    -infile ${indir}/{REST_proc_unfilt.nii.gz}"[4]" |                               \
    grep "datavalues" > {outfile}_data.log
#TST (IT IS UNCLEAR HOW TO IMPLEMENT THIS SECTION)
test_obj_eq.py "{outfile}_data.log --tolerance "5e4" --ignore-regex "Execution time" 
test_different.py *_data.logs
