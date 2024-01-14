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

# where all our dicom folders are
dataRoot = '/Users/cgouldvanpraag/Library/CloudStorage/OneDrive-TheAlanTuringInstitute/E&S Grand Challenge - Documents/WS1 Ecosystem/stakeholder-mapping/sharepoint-list-downloads'

sharepoint_date = '2024-01-09'
filename_prefix = 'stakeholder-list-E&S-'
filename_extension = '.csv'

filename_read_companies = filename_prefix+'companies-'+sharepoint_date+filename_extension
filename_read_projects = filename_prefix+'projects-'+sharepoint_date+filename_extension
filename_read_people = filename_prefix+'people-'+sharepoint_date+filename_extension
filename_read_interactions = filename_prefix+'interactions-'+sharepoint_date+filename_extension

filename_write = 'kumu-data-es-processed-'+sharepoint_date+'.xlsx'
path_write = os.path.join(dataRoot,filename_write)

path_read_companies = os.path.join(dataRoot,filename_read_companies)
path_read_projects = os.path.join(dataRoot,filename_read_projects)
path_read_people = os.path.join(dataRoot,filename_read_people)
# path_read_interactions = os.path.join(dataRoot,filename_read_interactions) # Not working with interactions yet. Will need to incorporate this data into 'people' metadata


# csv file containing our index of scan IDs
# data_people = pd.read_excel(path_read,sheet_name='people')
data_people = pd.read_csv(path_read_people)
data_companies = pd.read_csv(path_read_companies)
data_projects = pd.read_csv(path_read_projects)
# data_interactions = pd.read_csv(path_read_interactions)

data_elements = pd.DataFrame()
data_connections = pd.DataFrame()

print(data_people)
print(data_companies)
print(data_projects)


# First column in each table is the entry name in sharepoint.
# Rename to "label" for kumu

data_people = data_people.rename(columns={'name-person': 'label'})
data_companies = data_companies.rename(columns={'name-company': 'label'})
data_projects = data_projects.rename(columns={'name-project': 'label'})
                                                
print(data_people)
print(data_companies)
print(data_projects)

# Column names are different across the lists. Need to merge them together so all data types have the same metadata fields.
# You need to merge on all the common columns and use outer join (https://stackoverflow.com/questions/42940507/merging-dataframes-keeping-all-items-pandas)
# pd.merge(df1, df2, on = ['Name', 'Parent', 'Parent_Addr'], how = 'outer')
# find unique column headers over all dfs


# (https://stackoverflow.com/questions/59940311/retrieve-unique-column-names-over-multiple-dataframes-and-append-all-to-a-list)
alldf = [data_people, data_companies, data_projects]
desiredlist = []
for index, dataframe in enumerate(alldf):
    a = dataframe.columns.values.tolist()
    for column_name in a:
        if not column_name in desiredlist:
            desiredlist.append(column_name)

# combine data for "elements" tab
data_elements = pd.merge(data_people,data_companies, on = 'label', how = 'outer')
data_elements = pd.merge(data_elements,data_projects, on = 'label', how = 'outer')

data_elements.columns = data_elements.columns.str.rstrip('_x')  # strip suffix at the right end only.
data_elements.columns = data_elements.columns.str.rstrip('_y')  # strip suffix at the right end only.

def sjoin(x): return ';'.join(x[x.notnull()].astype(str))
data_elements = data_elements.groupby(level=0, axis=1).apply(lambda x: x.apply(sjoin, axis=1))

# move 'label' to first column
# (https://stackoverflow.com/questions/25122099/move-column-by-name-to-front-of-table-in-pandas)
cols = list(data_elements)
# move the column to head of list using index, pop and insert
cols.insert(0, cols.pop(cols.index('label')))
# use ix to reorder
data_elements = data_elements.loc[:, cols]


# Kumu: If you want to store multiple values inside of one cell (for example, tags or keywords), 
# just separate each value with the pipe character |. 

data_elements['affiliations'] = data_elements['affiliations'].str.replace(',','|')
data_elements['affiliations-turing'] = data_elements['affiliations-turing'].str.replace(',','|')
data_elements['projects'] = data_elements['projects'].str.replace(',','|')
data_elements['interaction-participant-all'] = data_elements['interaction-participant-all'].str.replace(',','|')
data_elements['interaction-participant-active'] = data_elements['interaction-participant-active'].str.replace(',','|')
data_elements['interaction-participant-presenter'] = data_elements['interaction-participant-presenter'].str.replace(',','|')
data_elements['interaction-participant-leadership'] = data_elements['interaction-participant-leadership'].str.replace(',','|')

data_elements['workstreams'] = data_elements['workstreams'].str.replace(',','|')
data_elements['workstreams'] = data_elements['workstreams'].str.replace('"','')
data_elements['workstreams'] = data_elements['workstreams'].str.replace('[','')
data_elements['workstreams'] = data_elements['workstreams'].str.replace(']','')

# create a new column "type-what" as a copy of "type" for kumu filtering (kumu doesn't seemto like to work with "type" alone for colour etc. )
data_elements['type-what'] = data_elements.loc[:, 'type']

# reorder columns so they are logical in kumu
def swap_columns(df, col1, col2):
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df

col_order = pd.Series(data_elements.columns)
print(col_order)

fix_cols = input("do you need to update the colomn order? (enter 0 or col number to by updated):")
while int(fix_cols) > 0:
    i = int(fix_cols)
    # ask which column you want in position i
    inputq = "what do you want in col" + str(i) + "? (type current index number):"
    x = int(input(inputq))
    # get the name of the col in position i
    col_new = col_order.iloc[x]
    # get the name of the column cirrently in position i
    col_old = col_order.iloc[i]
    # swap _old with _new
    data_elements = swap_columns(data_elements, col_old, col_new)
    col_order = pd.Series(data_elements.columns)
    print(col_order)
    fix_cols = input("do you need to update the colomn order? (enter 0 or col number to by updated):")


# create a new column "type-what" as a copy of "type" for kumu filtering
data_elements['type-what'] = data_elements.loc[:, 'type']

# Now handel the connections!!!

data_people['affiliations'] = data_people['affiliations'].str.replace(',','|')
data_people['affiliations-turing'] = data_people['affiliations-turing'].str.replace(',','|')
data_people['projects'] = data_people['projects'].str.replace(',','|')

data_people['workstreams'] = data_people['workstreams'].str.replace(',','|')
data_people['workstreams'] = data_people['workstreams'].str.replace('"','')
data_people['workstreams'] = data_people['workstreams'].str.replace('[','')
data_people['workstreams'] = data_people['workstreams'].str.replace(']','')

# print(data_people[['affiliations']].to_string(index=False)) 
# print(data_people[['affiliations-turing']].to_string(index=False)) 
# print(data_people[['projects']].to_string(index=False)) 
# print(data_people[['workstreams']].to_string(index=False)) 

# Kumu: If you put multiple elements in the "To" cell of a connection, separating each element with the pipe character |, 
# Kumu will draw a connection from the "From" element to each separate element in the "To" cell. (https://docs.kumu.io/guides/import/import)

# concatenate the affiliations and projects if not empty
data_people['to'] = data_people[['affiliations', 'affiliations-turing', 'projects']].apply(lambda x: ','.join(x.dropna()), axis=1)

# replace ',' in 'to' with |
data_people['to'] = data_people['to'].str.replace(',[]','')
data_people['to'] = data_people['to'].str.replace(',','|')
# replace 'Alan Turing Institute|Turing-' with 'Turing-'
data_people['to'] = data_people['to'].str.replace('Alan Turing Institute|Turing-','Turing-')

# rename 'label' to 'from'
data_people = data_people.rename(columns={'label': 'from'})
# keep only 'from' and 'to'
data_people = data_people[['from', 'to']]
# add 'direction' column ("undriected")
data_people['direction'] = 'undirected'


# DO IT ALL AGAIN FOR CONNECTIONS FOR COMPANIES AND PROJECTS

# 1. Merge affiliations
data_companies['affiliations'] = data_companies['affiliations'].str.replace(',','|')
data_projects['affiliations'] = data_projects['affiliations'].str.replace(',','|')

# 2. rename 'label' to 'from'
data_companies = data_companies.rename(columns={'label': 'from'})
data_projects = data_projects.rename(columns={'label': 'from'})

# 3. rename 'affiliations' to 'to'
data_companies = data_companies.rename(columns={'affiliations': 'to'})
data_projects = data_projects.rename(columns={'affiliations': 'to'})

# 4. keep only 'from' and 'to'
data_companies = data_companies[['from', 'to']]
data_projects = data_projects[['from', 'to']]

# 5. add 'undirected'
data_companies['direction'] = 'undirected'
data_projects['direction'] = 'undirected'

# COMBINE ALL THE CONNECTIONS

frames = [data_people, data_companies, data_projects]
data_connections = pd.concat(frames)

# replace NaN in 'to' with '[]'
data_connections['to'] = data_connections['to'].fillna('[]')

print('writing data to:' + path_write)
with pd.ExcelWriter(path_write) as writer:
    # use to_excel function and specify the sheet_name and index 
    # to store the dataframe in specified sheet
    data_elements.to_excel(writer, sheet_name="elements", index=False)
    data_connections.to_excel(writer, sheet_name="connections", index=False)
print('writing data - complete')    


# %%%%%%%%%%%%%%%%%%%%%%%%%%%
# Kumu display settings:
# @controls {
#   top-left {
#     search {}

#     showcase {
#       target: element;
#       by: "element type";
#       as: buttons;
#       multiple: true;
#       default: select-none;
#       mode: normal;
#       label: "showcase by affiliation type";
#     }

#     filter {
#       target: element;
#       by: "type-what";
#       as: buttons;
#       multiple: true;
#       default: show-all;
#       label: "filter by affiliation type";
#     }

#     filter {
#       target: element;
#       by: "interaction-participant-all";
#       as: buttons;
#       multiple: true;
#       default: show-all;
#       label: "filter by interaction-participant-all";
#     }
#   }
# }

# @settings {
#   template: stakeholder;
#   element-scale: scale("size", 0.5, 3);
#   element-color: categorize("type-what", neon2);
#   element-shape: categorize("type-what");
# }







# %%%%%%%%%%%%%%%%%%%%%%%%%%%





# old code
# # looping over each row in the people list using the index 'n'
# print('kumu >> Creating affiliation and project connections for ' + str(len(data_people)) + ' people')
# for index, n in data_people.iterrows():
#     connections_name = pd.DataFrame(columns=['From', 'To', 'Direction'])
    
#     name = n["label"]
#     print('kumu >> Processing person: ' + name)

#     # create the data for the affiliation connections
#     name_affiliation1 = n["Affiliation1"]
#     name_department = n["Department/Group/Team/Project"]
#     if name_affiliation1 == 'Alan Turing Institute' and isinstance(name_department,str):
#         connections_name = connections_name._append({'From' : name, 'To' : name_department, 'Direction' : 'undirected'}, ignore_index = True)
#     else:
#         connections_name = connections_name._append({'From' : name, 'To' : name_affiliation1, 'Direction' : 'undirected'}, ignore_index = True)

#     name_affiliation2 = n["Affiliation2"]
#     if isinstance(name_affiliation2,str):
#         connections_name = connections_name._append({'From' : name, 'To' : name_affiliation2, 'Direction' : 'undirected'}, ignore_index = True)

#     name_affiliation3 = n["Affiliation3"]
#     if isinstance(name_affiliation3,str):
#         connections_name = connections_name._append({'From' : name, 'To' : name_affiliation3, 'Direction' : 'undirected'}, ignore_index = True)

#     # create the data for the project connections
#     name_project1 = n["ResearchProjects1"]
#     if isinstance(name_project1,str):
#         connections_name = connections_name._append({'From' : name, 'To' : name_project1, 'Direction' : 'undirected'}, ignore_index = True)

#     name_project2 = n["ResearchProjects2"]
#     if isinstance(name_project2,str):
#         connections_name = connections_name._append({'From' : name, 'To' : name_project2, 'Direction' : 'undirected'}, ignore_index = True)

#     name_project3 = n["ResearchProjects3"]
#     if isinstance(name_project3,str):
#         connections_name = connections_name._append({'From' : name, 'To' : name_project3, 'Direction' : 'undirected'}, ignore_index = True)

#     name_project4 = n["ResearchProjects4"]
#     if isinstance(name_project4,str):
#         connections_name = connections_name._append({'From' : name, 'To' : name_project4, 'Direction' : 'undirected'}, ignore_index = True)

#     # write out connections to combined data (if any connections were created)
#     if not connections_all.empty:
#         connections_all = pd.concat([connections_all,connections_name],ignore_index=True, axis=0)
#     else:
#         connections_all = connections_name
#     # print(connections_all)
#     print('kumu >> Number of connections: ' + str(len(connections_name)))

# print(connections_all)

# # looping over each row in the companies list using the index 'c'
# print('kumu >> Creating affiliation connections for ' + str(len(data_companies)) + ' companies/organisations')
# for index, c in data_companies.iterrows():
#     connections_company = pd.DataFrame()
#     company = c["label"]
#     print('kumu >> Processing company/org: ' + company)

#     # create the data for the affiliation connections
#     company_affiliation1 = c["Affiliation1"]
#     if isinstance(company_affiliation1,str):
#         connections_company = connections_company._append({'From' : company, 'To' : company_affiliation1, 'Direction' : 'undirected'}, ignore_index = True)

#     company_affiliation2 = c["Affiliation2"]
#     if isinstance(company_affiliation2,str):
#         connections_company = connections_company._append({'From' : company, 'To' : company_affiliation2, 'Direction' : 'undirected'}, ignore_index = True)

#     company_affiliation3 = c["Affiliation3"]
#     if isinstance(company_affiliation3,str):
#         connections_company = connections_company._append({'From' : company, 'To' : company_affiliation3, 'Direction' : 'undirected'}, ignore_index = True)

#     # write out connections to combined data (if any connections were created)
#     if not connections_all.empty:
#         connections_all = pd.concat([connections_all,connections_company],ignore_index=True, axis=0)
#     else:
#         connections_all = connections_company
#     # print(connections_all)
#     print('kumu >> Number of connections: ' + str(len(connections_company)))

# # looping over each row in the projects list using the index 'p'
# print('kumu >> Creating affiliation connections for ' + str(len(data_projects)) + ' projects')
# for index, p in data_projects.iterrows():
#     connections_project = pd.DataFrame()
#     project = p["label"]
#     print('kumu >> Processing project: ' + project)

#     # create the data for the affiliation connections
#     project_affiliation1 = p["Affiliation1"]
#     if isinstance(project_affiliation1,str):
#         connections_project = connections_project._append({'From' : project, 'To' : project_affiliation1, 'Direction' : 'undirected'}, ignore_index = True)

#     project_affiliation2 = p["Affiliation2"]
#     if isinstance(project_affiliation2,str):
#         connections_project = connections_project._append({'From' : project, 'To' : project_affiliation2, 'Direction' : 'undirected'}, ignore_index = True)

#     project_affiliation3 = p["Affiliation3"]
#     if isinstance(project_affiliation3,str):
#         connections_project = connections_project._append({'From' : project, 'To' : project_affiliation3, 'Direction' : 'undirected'}, ignore_index = True)
    
  
#     # write out connections to combined data (if any connections were created)
#     if not connections_all.empty:
#         connections_all = pd.concat([connections_all,connections_project],ignore_index=True, axis=0)
#     else:
#         connections_all = connections_project
#     # print(connections_all)
#     print('kumu >> Number of connections: ' + str(len(connections_project)))

# # Print elements and connections to xlsx
# # elements_all.to_excel('/Users/cgouldvanpraag/Desktop/kumu-test.xlsx', sheet_name='elements', index=False)
# # connections_all.to_excel('/Users/cgouldvanpraag/Desktop/kumu-test.xlsx', sheet_name='connections', index=False)


# with pd.ExcelWriter(path_write) as writer:
#     # use to_excel function and specify the sheet_name and index 
#     # to store the dataframe in specified sheet
#     elements_all.to_excel(writer, sheet_name="elements", index=False)
#     connections_all.to_excel(writer, sheet_name="connections", index=False)

# print('kumu >> Total number of elements: ' + str(len(elements_all)))
# print('kumu >> Total number of connections: ' + str(len(connections_all)))