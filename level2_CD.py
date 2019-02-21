import os
import shutil
from os.path import abspath
from os.path import join as opj
from nipype.interfaces.io import SelectFiles, DataSink
from nipype.interfaces.spm import (OneSampleTTestDesign, EstimateModel,
                                   EstimateContrast, Threshold)
from nipype.interfaces.utility import IdentityInterface
from nipype import Workflow, Node
from nipype.interfaces.fsl import Info
from nipype.algorithms.misc import Gunzip
import nipype.interfaces.matlab as mlab
matlab_cmd = ''


mlab.MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")
        # If SPM is not in your MATLAB path you should add it here
matlab_cmd = 'users/dima/Applications/MATLAB_R2018ba.app/bin/matlab'

project_path = abspath('../data')


data_dir = os.path.abspath('../data')
project_dir = os.path.abspath
output_dir = os.path.abspath('../data/derivatives/SPM')
working_dir = os.path.abspath('../data/derivatives/SPM/level2/workdir_C_D')
preproc_dir = os.path.abspath('preproc')
mask = abspath('../data/derivatives/SPM/level2/group_mask.nii')

contrast_id_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
for i in contrast_id_list:
    con_id = i



    import json
    from os.path import isfile
    from os import listdir
    from glob import glob
    import os
    from os.path import abspath
    data_dir = os.path.abspath('../data')


    conlist = []
    import json
    with open("CD.json") as f:
        groups = json.load(f)

    for key, value in groups.items():
        subject_id = key
        for run_id in list(value):

            results = os.path.join(data_dir, "derivatives", "SPM", "level1",
                                       "sub-%s" % subject_id, "run-0%s" % run_id, "con_000%s.nii" % con_id)
            if isfile(results):
                conlist.append(results)

    # OneSampleTTestDesign - creates one sample T-Test Design
    onesamplettestdes = Node(OneSampleTTestDesign(),
                             name="onesampttestdes")
    onesamplettestdes.inputs.in_files = conlist
    onesamplettestdes.inputs.explicit_mask_file = mask


    # EstimateModel - estimates the model
    level2estimate = Node(EstimateModel(estimation_method={'Classical': 1}),
                          name="level2estimate")

    # EstimateContrast - estimates group contrast
    level2conestimate = Node(EstimateContrast(group_contrast=True),
                             name="level2conestimate")
    cont1 = ['Group', 'T', ['mean'], [1]]
    level2conestimate.inputs.contrasts = [cont1]

    # Threshold - thresholds contrasts
    level2thresh = Node(Threshold(contrast_index=1,
                                  use_topo_fdr=True,
                                  use_fwe_correction=False,
                                  extent_threshold=0,
                                  height_threshold=0.005,
                                  height_threshold_type='p-value',
                                  extent_fdr_p_threshold=0.05),
                        name="level2thresh")
    # Datasink - creates output folder for important outputs
    datasink = Node(DataSink(base_directory=output_dir, parameterization=False,
                                     container='level2/C_D_group_all_cons/con_%s' % con_id),
                            name="datasink")

    # Initiation of the 2nd-level analysis workflow
    l2analysis = Workflow(name='level2')
    l2analysis.base_dir = working_dir

    # Connect up the 2nd-level analysis components
    l2analysis.connect([(onesamplettestdes, level2estimate, [('spm_mat_file',
                                                              'spm_mat_file')]),
                        (level2estimate, level2conestimate, [('spm_mat_file',
                                                              'spm_mat_file'),
                                                             ('beta_images',
                                                              'beta_images'),
                                                             ('residual_image',
                                                              'residual_image')]),
                        (level2conestimate, level2thresh, [('spm_mat_file',
                                                            'spm_mat_file'),
                                                           ('spmT_images',
                                                            'stat_image'),
                                                           ]),
                        (level2conestimate, datasink, [('spm_mat_file',
                                                        '@spm_mat'),
                                                       ('spmT_images',
                                                        '@T'),
                                                       ('con_images',
                                                        '@con')]),
                        (level2thresh, datasink, [('thresholded_map',
                                                   '@threshold')]),
                        ])

    # Create 1st-level analysis output graph
    l2analysis.write_graph(graph2use='colored', format='png', simple_form=True)

    # Visualize the graph
    from IPython.display import Image
    Image(filename=opj(l2analysis.base_dir, 'level2', 'graph.png'))

    l2analysis.run('MultiProc')

    shutil.rmtree(working_dir)

