######
import json
with open("AB.json") as f:
    groups = json.load(f)

for key, value in groups.items():
    subject_id = key
    for i in list(value):
        run_id = i
        print('running for subject  ' + subject_id + '  run ' + run_id)

        ######

        # Import modules

        #####
        import os
        from os.path import abspath
        from bids import BIDSLayout
        from nipype.pipeline.engine import Workflow, Node
        from nipype.interfaces.io import DataSink, DataGrabber
        from nipype.interfaces.base import Bunch
        import nipype.interfaces.matlab as mlab  # how to run matlab
        matlab_cmd = ''
        from nipype.algorithms.modelgen import SpecifySPMModel
        from nipype.interfaces.spm import Smooth, Level1Design, EstimateModel, EstimateContrast
        from nipype.algorithms.misc import Gunzip
        from nipype.interfaces.fsl import ExtractROI

        import shutil

        #####

        # Set variables

        ####

        mlab.MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")
        # If SPM is not in your MATLAB path you should add it here
        matlab_cmd = 'users/dima/Applications/MATLAB_R2018ba.app/bin/matlab'

        project_path = abspath('../data')

        layout = BIDSLayout(project_path)
        data_dir = os.path.abspath('../data')
        project_dir = os.path.abspath


        contrast_0 = ['A', 'T', [u'A', u'OFF'], [1, -1]]
        contrast_1 = ['B', 'T', [u'A', u'OFF'], [1, -1]]
        contrast_2 = ['A>B', 'T', [u'A', u'B'], [1, -1]]
        contrast_3 = ['B>A', 'T', [u'A', u'B'], [-1, 1]]
        contrasts = [contrast_0, contrast_1, contrast_2, contrast_3]

        output_dir = os.path.abspath('../data/derivatives/SPM')
        working_dir = os.path.abspath('../data/derivatives/SPM/workdir')
        preproc_dir = os.path.abspath('preproc')

        import pandas as pd

        events = pd.read_csv(os.path.join(data_dir, "sub-%s" % subject_id, "func",
                                          "sub-%s_task-odormixture_run-0%s_events.tsv") % (subject_id, run_id),
                             sep="\t")

        confounds = pd.read_csv(os.path.join(data_dir, "derivatives", "fmriprep",
                                             "sub-%s" % subject_id, "func",
                                             "sub-%s_task-odormixture_run-0%s_bold_confounds.tsv"
                                             % (subject_id, run_id)),
                                sep="\t", na_values="n/a")

        info = [Bunch(conditions=['A',
                                  'B',
                                  'OFF'],
                      onsets=[list(events[events.trial_type == 'A'].onset -6),
                              list(events[events.trial_type == 'B'].onset -6),
                              list(events[events.trial_type == 'OFF'].onset -6)],
                      durations=[list(events[events.trial_type == 'A'].duration),
                                 list(events[events.trial_type == 'B'].duration),
                                 list(events[events.trial_type == 'OFF'].duration)],
                      regressors=[list(confounds.FramewiseDisplacement[3:]),
                                  list(confounds.aCompCor00[3:]),
                                  list(confounds.aCompCor01[3:]),
                                  list(confounds.aCompCor02[3:]),
                                  list(confounds.aCompCor03[3:]),
                                  list(confounds.aCompCor04[3:]),
                                  list(confounds.aCompCor05[3:]),
                                  ],
                      regressor_names=['FramewiseDisplacement',
                                       'aCompCor0',
                                       'aCompCor1',
                                       'aCompCor2',
                                       'aCompCor3',
                                       'aCompCor4',
                                       'aCompCor5', ],
                      amplitudes=None,
                      tmod=None,
                      pmod=None)
                ]

        ####

        ####

        # Set Nodes

        ####

        preproc_folder = '/Users/dima/Desktop/odormixture/data/derivatives/fmriprep'

        field_template = {
            'func': 'sub-%s/func/sub-%s_task-odormixture_run-0%s_bold_space-MNI152NLin2009cAsym_preproc.nii.gz',
            'mask': 'sub-%s/func/sub-%s_task-odormixture_run-0%s_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz'}
        template_args = {'func': [[subject_id, subject_id, run_id]],
                         'mask': [[subject_id, subject_id, run_id]]}

        datasource = Node(interface=DataGrabber(infields=['subject_id', 'run_id'], outfields=['func', 'mask']),
                          name='datasource')
        datasource.inputs.base_directory = preproc_folder
        datasource.inputs.template = '*'
        datasource.inputs.field_template = field_template
        datasource.inputs.template_args = template_args
        datasource.inputs.sort_filelist = False
        datasource.inputs.subject_id = subject_id
        datasource.inputs.run_id = run_id

        gunzip_func = Node(Gunzip(), name='gunzip_func')
        gunzip_mask = Node(Gunzip(), name='gunzip_mask')


        smooth = Node(Smooth(), name='smooth')
        smooth.inputs.fwhm = [4, 4, 4]

        fsl_roi = Node(ExtractROI(t_min=3, t_size=-1, output_type='NIFTI'), name='fsl_roi')

        modelspec = Node(SpecifySPMModel(concatenate_runs=False,
                                         input_units='secs',
                                         output_units='secs',
                                         time_repetition= 2,
                                         high_pass_filter_cutoff=128),
                         name="modelspec")
        modelspec.inputs.subject_info = info

        level1design = Node(Level1Design(bases={'hrf': {'derivs': [0, 0]}},
                                         timing_units='secs',
                                         interscan_interval = 2,
                                         model_serial_correlations='AR(1)'),
                            name="level1design")

        EstimateModel = Node(EstimateModel(estimation_method={'Classical': 1}),
                             name="EstimateModel")

        level1conest = Node(EstimateContrast(), name="level1conest")
        level1conest.inputs.contrasts = contrasts

        datasink = Node(DataSink(base_directory=output_dir, parameterization=False,
                                 container='level1/sub-%s/run-0%s' % (subject_id, run_id)),
                        name="datasink")

        output = Node(DataSink(parameterization=False), name='level1')
        output.inputs.base_directory = output_dir

        ###

        # connect workflow

        ###

        level1 = Workflow(name='level1')
        level1.base_dir = working_dir
        level1.connect([
            (datasource, gunzip_func, [('func', 'in_file')]),
            (datasource, gunzip_mask, [('mask', 'in_file')]),
            (gunzip_func, smooth, [('out_file', 'in_files')]),
            (gunzip_mask, level1design, [('out_file', 'mask_image')]),
            (smooth, fsl_roi, [('smoothed_files', 'in_file')]),
            (fsl_roi, modelspec, [('roi_file', 'functional_runs')]),
            (modelspec, level1design, [('session_info', 'session_info')]),
            (level1design, EstimateModel, [('spm_mat_file', 'spm_mat_file')]),
            (EstimateModel, level1conest, [('spm_mat_file', 'spm_mat_file')]),
            (EstimateModel, level1conest, [('beta_images', 'beta_images')]),
            (EstimateModel, level1conest, [('residual_image', 'residual_image')]),
            (EstimateModel, datasink, [('mask_image', '@mask')]),
            (level1conest, datasink, [('spm_mat_file', '@spm_mat'),
                                      ('spmT_images', '@T'),
                                      ('con_images', '@con'),
                                      ('spmF_images', '@F'),
                                      ('ess_images', '@ess'),
                                      ]),
        ])

        level1.write_graph(graph2use='flat', format='svg', simple_form=True)

        ###

        # run the workflow

        ###
        level1.run()
        shutil.rmtree(working_dir)
