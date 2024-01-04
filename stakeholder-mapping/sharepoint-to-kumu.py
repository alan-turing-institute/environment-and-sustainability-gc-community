# kumu-connections-tric-dt.py
# This script reads in an xlsx file of stakeholder metadata and prepares a file for kumu mapping.

# # Set-up in terminal
# Adapted from [TTW local build step-by-step guide](https://the-turing-way.netlify.app/community-handbook/local-build.html?highlight=conda%20env) to use a conda environment
# 1. [install miniconda](https://docs.conda.io/projects/miniconda/en/latest/)
# 2. `conda init`
# 3. `curl https://git.fmrib.ox.ac.uk/paulmc/grad_course_2019_python_intro/raw/master/env.yml` > kumu-env.yml
# 4. `conda env create -f kumu-env.yml`
# 5. `conda activate kumu_env`
# 6. in vs code, set python interpreter to kumu_env before running debugging




# library of functions for checking, makeing, renaming files etc.
import os as os
import subprocess
# subprocess.run('source activate the-turing-way', shell=True)
# subprocess.run('pwd', shell=True)
# subprocess.run('pip install -r requirements.txt',shell=True)
# library for handelling data read in from the xlsx file
import pandas as pd
import numpy as np

# where all our dicom folders are
dataRoot = '/Users/cgouldvanpraag/Documents/OneDrive - The Alan Turing Institute/TRIC-DT-team/Hub/stakeholder-mapping/kumu'
filename_read = 'kumu-data-tric-dt.xlsx'
filename_write = 'kumu-data-tric-dt-processed.xlsx'

path_read = os.path.join(dataRoot,filename_read)
path_write = os.path.join(dataRoot,filename_write)

# csv file containing our index of scan IDs
data_people = pd.read_excel(path_read,sheet_name='people')
data_companies = pd.read_excel(path_read,sheet_name='companies')
data_projects = pd.read_excel(path_read,sheet_name='projects')
data_interactions = pd.read_excel(path_read,sheet_name='interactions') # NOT DOING ANYTHING WITH INTERACTIONS YET
data_interactions = pd.read_excel(path_read,sheet_name='funders') # NOT DOING ANYTHING WITH FUNDERS YET (need to think about how to include them in the column headers)

data_connections = pd.DataFrame()


# combine data for "elements" tab
elements_all = pd.concat([data_people,data_companies,data_projects],ignore_index=True, axis=0)
connections_all = pd.DataFrame()

# looping over each row in the people list using the index 'n'
print('kumu >> Creating affiliation and project connections for ' + str(len(data_people)) + ' people')
for index, n in data_people.iterrows():
    connections_name = pd.DataFrame(columns=['From', 'To', 'Direction'])
    
    name = n["label"]
    print('kumu >> Processing person: ' + name)

    # create the data for the affiliation connections
    name_affiliation1 = n["Affiliation1"]
    name_department = n["Department/Group/Team/Project"]
    if name_affiliation1 == 'Alan Turing Institute' and isinstance(name_department,str):
        connections_name = connections_name._append({'From' : name, 'To' : name_department, 'Direction' : 'undirected'}, ignore_index = True)
    else:
        connections_name = connections_name._append({'From' : name, 'To' : name_affiliation1, 'Direction' : 'undirected'}, ignore_index = True)

    name_affiliation2 = n["Affiliation2"]
    if isinstance(name_affiliation2,str):
        connections_name = connections_name._append({'From' : name, 'To' : name_affiliation2, 'Direction' : 'undirected'}, ignore_index = True)

    name_affiliation3 = n["Affiliation3"]
    if isinstance(name_affiliation3,str):
        connections_name = connections_name._append({'From' : name, 'To' : name_affiliation3, 'Direction' : 'undirected'}, ignore_index = True)

    # create the data for the project connections
    name_project1 = n["ResearchProjects1"]
    if isinstance(name_project1,str):
        connections_name = connections_name._append({'From' : name, 'To' : name_project1, 'Direction' : 'undirected'}, ignore_index = True)

    name_project2 = n["ResearchProjects2"]
    if isinstance(name_project2,str):
        connections_name = connections_name._append({'From' : name, 'To' : name_project2, 'Direction' : 'undirected'}, ignore_index = True)

    name_project3 = n["ResearchProjects3"]
    if isinstance(name_project3,str):
        connections_name = connections_name._append({'From' : name, 'To' : name_project3, 'Direction' : 'undirected'}, ignore_index = True)

    name_project4 = n["ResearchProjects4"]
    if isinstance(name_project4,str):
        connections_name = connections_name._append({'From' : name, 'To' : name_project4, 'Direction' : 'undirected'}, ignore_index = True)

    # write out connections to combined data (if any connections were created)
    if not connections_all.empty:
        connections_all = pd.concat([connections_all,connections_name],ignore_index=True, axis=0)
    else:
        connections_all = connections_name
    # print(connections_all)
    print('kumu >> Number of connections: ' + str(len(connections_name)))

print(connections_all)

# looping over each row in the companies list using the index 'c'
print('kumu >> Creating affiliation connections for ' + str(len(data_companies)) + ' companies/organisations')
for index, c in data_companies.iterrows():
    connections_company = pd.DataFrame()
    company = c["label"]
    print('kumu >> Processing company/org: ' + company)

    # create the data for the affiliation connections
    company_affiliation1 = c["Affiliation1"]
    if isinstance(company_affiliation1,str):
        connections_company = connections_company._append({'From' : company, 'To' : company_affiliation1, 'Direction' : 'undirected'}, ignore_index = True)

    company_affiliation2 = c["Affiliation2"]
    if isinstance(company_affiliation2,str):
        connections_company = connections_company._append({'From' : company, 'To' : company_affiliation2, 'Direction' : 'undirected'}, ignore_index = True)

    company_affiliation3 = c["Affiliation3"]
    if isinstance(company_affiliation3,str):
        connections_company = connections_company._append({'From' : company, 'To' : company_affiliation3, 'Direction' : 'undirected'}, ignore_index = True)

    # write out connections to combined data (if any connections were created)
    if not connections_all.empty:
        connections_all = pd.concat([connections_all,connections_company],ignore_index=True, axis=0)
    else:
        connections_all = connections_company
    # print(connections_all)
    print('kumu >> Number of connections: ' + str(len(connections_company)))

# looping over each row in the projects list using the index 'p'
print('kumu >> Creating affiliation connections for ' + str(len(data_projects)) + ' projects')
for index, p in data_projects.iterrows():
    connections_project = pd.DataFrame()
    project = p["label"]
    print('kumu >> Processing project: ' + project)

    # create the data for the affiliation connections
    project_affiliation1 = p["Affiliation1"]
    if isinstance(project_affiliation1,str):
        connections_project = connections_project._append({'From' : project, 'To' : project_affiliation1, 'Direction' : 'undirected'}, ignore_index = True)

    project_affiliation2 = p["Affiliation2"]
    if isinstance(project_affiliation2,str):
        connections_project = connections_project._append({'From' : project, 'To' : project_affiliation2, 'Direction' : 'undirected'}, ignore_index = True)

    project_affiliation3 = p["Affiliation3"]
    if isinstance(project_affiliation3,str):
        connections_project = connections_project._append({'From' : project, 'To' : project_affiliation3, 'Direction' : 'undirected'}, ignore_index = True)
    
  
    # write out connections to combined data (if any connections were created)
    if not connections_all.empty:
        connections_all = pd.concat([connections_all,connections_project],ignore_index=True, axis=0)
    else:
        connections_all = connections_project
    # print(connections_all)
    print('kumu >> Number of connections: ' + str(len(connections_project)))

# Print elements and connections to xlsx
# elements_all.to_excel('/Users/cgouldvanpraag/Desktop/kumu-test.xlsx', sheet_name='elements', index=False)
# connections_all.to_excel('/Users/cgouldvanpraag/Desktop/kumu-test.xlsx', sheet_name='connections', index=False)


with pd.ExcelWriter(path_write) as writer:
    # use to_excel function and specify the sheet_name and index 
    # to store the dataframe in specified sheet
    elements_all.to_excel(writer, sheet_name="elements", index=False)
    connections_all.to_excel(writer, sheet_name="connections", index=False)

print('kumu >> Total number of elements: ' + str(len(elements_all)))
print('kumu >> Total number of connections: ' + str(len(connections_all)))