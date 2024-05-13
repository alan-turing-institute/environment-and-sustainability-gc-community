# kumu-connections-tric-dt.py
# This script reads in an xlsx file of stakeholder metadata and prepares a file for kumu mapping.

# # Set-up in terminal
# Adapted from [TTW local build step-by-step guide](https://the-turing-way.netlify.app/community-handbook/local-build.html?highlight=conda%20env) to use a conda environment
# 1. [install miniconda](https://docs.conda.io/projects/miniconda/en/latest/)
# 2. `conda init`
# 3. `curl https://git.fmrib.ox.ac.uk/paulmc/grad_course_2019_python_intro/raw/master/env.yml` > kumu-env.yml
# 4. `conda env create -f kumu-env.yml`
# 5. `conda activate kumu_env`
# 6. in vs code, set python interpreter to kumu_env before running debugging (see [guide here](https://code.visualstudio.com/docs/python/environments#_using-the-create-environment-command))




# library of functions for checking, makeing, renaming files etc.
import os as os
import subprocess
# subprocess.run('source activate the-turing-way', shell=True)
# subprocess.run('pwd', shell=True)
# subprocess.run('pip install -r requirements.txt',shell=True)
# library for handelling data read in from the xlsx file
import pandas as pd
import numpy as np
import csv
from anonymizedf.anonymizedf import anonymize
import time
import json

# where all our data is
dataRoot = '/Users/cgouldvanpraag/Library/CloudStorage/OneDrive-TheAlanTuringInstitute/E&S Grand Challenge - Documents/WS1 Ecosystem/stakeholder-mapping/data-sources/'

sharepoint_date = '20240228'
filename_prefix = 'stakeholder-list-E&S-'
filename_extension = '.csv'

filename_slack_list = 'slack-turing-e-and-s3676489216549-members'
path_read_slack = os.path.join(dataRoot,'slack',filename_slack_list+'.csv')

filename_read_people = filename_prefix+'people-'+sharepoint_date+filename_extension

timestr = time.strftime("-%Y%m%d-%H%M%S")

filename_output_missing_persons = filename_slack_list+'-missing-from-sharepoint-people-'+sharepoint_date+timestr+'.xlsx'

path_output_missing_persons = os.path.join(dataRoot,'slack',filename_output_missing_persons)



path_read_people = os.path.join(dataRoot,'sharepoint-list-downloads',filename_read_people)
# path_read_interactions = os.path.join(dataRoot,filename_read_interactions) # Not working with interactions yet. Will need to incorporate this data into 'people' metadata

# csv file containing our index of scan IDs
# data_people = pd.read_excel(path_read,sheet_name='people')
data_people_sharepoint = pd.read_csv(path_read_people)
data_people_slack = pd.read_csv(path_read_slack)

# print(data_people_sharepoint)
# print(data_people_slack)

# First column in each table is the entry name in sharepoint.
# Rename to "label" for kumu

df1 = data_people_slack
df2 = data_people_sharepoint

missing_person_list = []
# missing_person = pd.DataFrame(columns=['slack-person-missing-from-sharepoint','slack-email'])

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# # Loop through df1 and find matching values in df2
print("Looking for matching email addresses from (reference) ",filename_slack_list, " in (comparison) ", filename_read_people)
for index, row in df1.iterrows():
    # print(index)
    # print(df1.iloc[index]) #df1.at[index, 'label-public']
    id_name = row['fullname']
    id_email = row['email']
    print('- PROCESSING: email-slack: ',id_email, '; name-slack: ', id_name)
    if index == 485:
        print('Found A Fuller')
    matching_row_email = df2[df2['email'] == id_email]
    if not matching_row_email.empty:
        match_sharepoint_ID = matching_row_email['ID'].values[0]
        print("- Found match for email-slack: ", id_email, "; name-slack: ", id_name," @ sharepointID", match_sharepoint_ID)
    else:
        matching_row_name = df2[df2['name-person'] == id_name]
        if not matching_row_name.empty:
            match_sharepoint_ID = matching_row_name['ID'].values[0]
            email_sp = matching_row_name['email'].values[0]
            missing_person_list.append([id_name, id_email,1,email_sp])
            print("- Found match for name-slack: ", id_name, "; email-sp: ", email_sp," @ sharepointID", match_sharepoint_ID)
        else:
            missing_person_list.append([id_name, id_email, np.nan,np.nan])
            print("** WARNING: No match found for email-slack: ", id_email, " or name-slack: ",id_name)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
# Convert missing_person list to DataFrame
# missing_person_df = pd.DataFrame({'slack-person-missing-from-sharepoint': missing_person})
missing_person = pd.DataFrame(missing_person_list, columns=['slack-person-missing-from-sharepoint', 'slack-email','sp-already-on','sp-email'])

print("Missing Persons:")
print(missing_person)

# Write the DataFrame to an Excel file
missing_person.to_excel(path_output_missing_persons, index=False)

# Print a message to confirm the file has been saved
print("DataFrame 'missing_person' has been successfully written to:", path_output_missing_persons)

# # write out
# print('writing anonymised data to:' + path_write_public)
# with pd.ExcelWriter(path_write_public) as writer:
#     # use to_excel function and specify the sheet_name and index 
#     # to store the dataframe in specified sheet
#     data_elements_anon.to_excel(writer, sheet_name="elements", index=False)
#     data_connections_anon.to_excel(writer, sheet_name="connections", index=False)
# print('writing xlsx data for public map - complete')


# #################



# # %%%%%%%%%%%%%%%%%%%%%%%%%%%



