# import modules

from os.path import abspath, join, pardir

from bids.layout import BIDSLayout

project_path = abspath("../data")

layout = BIDSLayout(project_path)



sublist1 = ['03', '04']
sublist2 = ['05', '06', '07']
sublist3 = ['09', '10', '11', '12']
sublist4 = ['13', '15', '16']
sublist5 = ['17', '18', '19', '20']
sublist6 = ['21', '23', '24']
sublist7 = ['25', '26', '27']
sublist8 = ['29', '30']



import pandas as pd
s1 = pd.read_csv('/Users/dima/Desktop/odormixture/description/tsv/s1.tsv', sep="\t")
s2 = pd.read_csv('/Users/dima/Desktop/odormixture/description/tsv/s2.tsv', sep="\t")
s3 = pd.read_csv('/Users/dima/Desktop/odormixture/description/tsv/s3.tsv', sep="\t")
s4 = pd.read_csv('/Users/dima/Desktop/odormixture/description/tsv/s4.tsv', sep="\t")
s5 = pd.read_csv('/Users/dima/Desktop/odormixture/description/tsv/s5.tsv', sep="\t")
s6 = pd.read_csv('/Users/dima/Desktop/odormixture/description/tsv/s6.tsv', sep="\t")


###########################################################################################################
# Group 1
###########################################################################################################


for subject_id in sublist1:
    run_id_1 = '3'
    run_id_2 = '5'
    session = s2

    #############
    # run_id_1


    subject_id = subject_id
    run_id = run_id_1

    file_path = join('/Users/dima/Desktop/odormixture/data/sub-%s/func/sub-%s_task-odormixture_run-0%s_events.tsv'
                     % (subject_id, subject_id, run_id))
    session.to_csv(file_path, sep="\t", index=False)


    #############
    # run_id_2

    run_id = run_id_2

    file_path = join('/Users/dima/Desktop/odormixture/data/sub-%s/func/sub-%s_task-odormixture_run-0%s_events.tsv'
                     % (subject_id, subject_id, run_id))
    session.to_csv(file_path, sep="\t", index=False)


# Group 2
###########################################################################################################


for subject_id in sublist2:
    run_id_1 = '3'
    run_id_2 = '5'
    session = s5

    #############
    # run_id_1

    subject_id = subject_id
    run_id = run_id_1

    file_path = join('/Users/dima/Desktop/odormixture/data/sub-%s/func/sub-%s_task-odormixture_run-0%s_events.tsv'
                     % (subject_id, subject_id, run_id))
    session.to_csv(file_path, sep="\t", index=False)

    #############
    # run_id_2

    run_id = run_id_2

    file_path = join('/Users/dima/Desktop/odormixture/data/sub-%s/func/sub-%s_task-odormixture_run-0%s_events.tsv'
                     % (subject_id, subject_id, run_id))
    session.to_csv(file_path, sep="\t", index=False)

###########################################################################################################
# Group 3
###########################################################################################################

for subject_id in sublist3:
    run_id_1 = '4'
    run_id_2 = '6'
    session = s2

    #############
    # run_id_1

    subject_id = subject_id
    run_id = run_id_1

    file_path = join('/Users/dima/Desktop/odormixture/data/sub-%s/func/sub-%s_task-odormixture_run-0%s_events.tsv'
                     % (subject_id, subject_id, run_id))
    session.to_csv(file_path, sep="\t", index=False)

    #############
    # run_id_2

    run_id = run_id_2

    file_path = join('/Users/dima/Desktop/odormixture/data/sub-%s/func/sub-%s_task-odormixture_run-0%s_events.tsv'
                     % (subject_id, subject_id, run_id))
    session.to_csv(file_path, sep="\t", index=False)

###########################################################################################################
# Group 4
###########################################################################################################


for subject_id in sublist4:
    run_id_1 = '4'
    run_id_2 = '6'
    session = s5


#############
    # run_id_1


    subject_id = subject_id
    run_id = run_id_1

    file_path = join('/Users/dima/Desktop/odormixture/data/sub-%s/func/sub-%s_task-odormixture_run-0%s_events.tsv'
                     % (subject_id, subject_id, run_id))
    session.to_csv(file_path, sep="\t", index=False)


    #############
    # run_id_2

    run_id = run_id_2

    file_path = join('/Users/dima/Desktop/odormixture/data/sub-%s/func/sub-%s_task-odormixture_run-0%s_events.tsv'
                     % (subject_id, subject_id, run_id))
    session.to_csv(file_path, sep="\t", index=False)


###########################################################################################################
# Group 5
###########################################################################################################

for subject_id in sublist5:
    run_id_1 = '1'
    run_id_2 = '3'
    session = s2

    #############
    # run_id_1

    subject_id = subject_id
    run_id = run_id_1

    file_path = join('/Users/dima/Desktop/odormixture/data/sub-%s/func/sub-%s_task-odormixture_run-0%s_events.tsv'
                     % (subject_id, subject_id, run_id))
    session.to_csv(file_path, sep="\t", index=False)

    #############
    # run_id_2

    run_id = run_id_2

    file_path = join('/Users/dima/Desktop/odormixture/data/sub-%s/func/sub-%s_task-odormixture_run-0%s_events.tsv'
                     % (subject_id, subject_id, run_id))
    session.to_csv(file_path, sep="\t", index=False)

###########################################################################################################
# Group 6
###########################################################################################################

for subject_id in sublist6:
    run_id_1 = '1'
    run_id_2 = '3'
    session = s5


#############
    # run_id_1


    subject_id = subject_id
    run_id = run_id_1

    file_path = join('/Users/dima/Desktop/odormixture/data/sub-%s/func/sub-%s_task-odormixture_run-0%s_events.tsv'
                     % (subject_id, subject_id, run_id))
    session.to_csv(file_path, sep="\t", index=False)


    #############
    # run_id_2

    run_id = run_id_2

    file_path = join('/Users/dima/Desktop/odormixture/data/sub-%s/func/sub-%s_task-odormixture_run-0%s_events.tsv'
                     % (subject_id, subject_id, run_id))
    session.to_csv(file_path, sep="\t", index=False)

###########################################################################################################
# Group 7
###########################################################################################################
for subject_id in sublist7:
    run_id_1 = '2'
    run_id_2 = '4'
    session = s2



#############
    # run_id_1


    subject_id = subject_id
    run_id = run_id_1

    file_path = join('/Users/dima/Desktop/odormixture/data/sub-%s/func/sub-%s_task-odormixture_run-0%s_events.tsv'
                     % (subject_id, subject_id, run_id))
    session.to_csv(file_path, sep="\t", index=False)


    #############
    # run_id_2

    run_id = run_id_2

    file_path = join('/Users/dima/Desktop/odormixture/data/sub-%s/func/sub-%s_task-odormixture_run-0%s_events.tsv'
                     % (subject_id, subject_id, run_id))
    session.to_csv(file_path, sep="\t", index=False)


###########################################################################################################
# Group 8
###########################################################################################################


for subject_id in sublist8:
    run_id_1 = '2'
    run_id_2 = '4'
    session = s5




#############
    # run_id_1


    subject_id = subject_id
    run_id = run_id_1

    file_path = join('/Users/dima/Desktop/odormixture/data/sub-%s/func/sub-%s_task-odormixture_run-0%s_events.tsv'
                     % (subject_id, subject_id, run_id))
    session.to_csv(file_path, sep="\t", index=False)


    #############
    # run_id_2

    run_id = run_id_2

    file_path = join('/Users/dima/Desktop/odormixture/data/sub-%s/func/sub-%s_task-odormixture_run-0%s_events.tsv'
                     % (subject_id, subject_id, run_id))
    session.to_csv(file_path, sep="\t", index=False)
