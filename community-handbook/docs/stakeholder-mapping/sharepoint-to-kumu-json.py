
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
import pandas as pd
import numpy as np
import csv
from anonymizedf.anonymizedf import anonymize
import time
import json

# where all our data is
dataRoot = '/Users/cgouldvanpraag/Library/CloudStorage/OneDrive-TheAlanTuringInstitute/E&S Grand Challenge - Documents/WS1 Ecosystem/stakeholder-mapping/data-sources/'

# the "-b" file has the ID column deleted
sharepoint_date = '20240220-noID'
filename_prefix = 'kumu-data-es-processed-'

path_read = os.path.join(dataRoot,'kumu',filename_prefix+sharepoint_date+'.xlsx')
path_write = os.path.join(dataRoot,'kumu',filename_prefix+sharepoint_date+'.json')

sheet_name='elements'
final_key='elements'

# with pd.ExcelWriter(path_write) as writer:
#     # use to_excel function and specify the sheet_name and index 
#     # to store the dataframe in specified sheet
#     data_elements.to_excel(writer, sheet_name="elements", index=False)
#     data_connections.to_excel(writer, sheet_name="connections", index=False)
# print('writing xlsx data - complete')    

# #################
# WRITE JSON

# data_elements_json = data_elements
# data_connections_json = data_connections

# replace bundled affiliaitons etc with syntax etc for json

def xlsx_to_nested_json(xlsx_file, json_file, sheet_name, nested_columns, final_key):
    # Read the specified Excel sheet into a pandas DataFrame
    df = pd.read_excel(xlsx_file, sheet_name=sheet_name)
    
    # Initialize an empty list to store nested data
    nested_data = []
    
    # Iterate over rows in the DataFrame
    for _, row in df.iterrows():
        for column in nested_columns:
            # Check if the column contains "|"
            if '|' in str(row[column]):
                # Split the column value based on "|"
                value_list = str(row[column]).split('|')
                # Remove leading and trailing spaces from each value
                value_list = [value.strip() for value in value_list]
                # Nest the values under the column name
                row[column] = value_list
        
        # Append the row to the nested_data list
        nested_data.append(row.to_dict())
    
    # Create a dictionary with the specified final key as the key and nested_data as the value
    json_data = {final_key: nested_data}
    
    # Convert the dictionary to JSON and save it to a file
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=4)

# Example usage:
# Replace 'input.xlsx' with the path to your Excel file
# Replace 'output.json' with the path where you want to save the JSON file
# Replace 'Sheet1' with the name of the Excel sheet you want to read
# Replace ['affiliations'] with a list of column names you want to process
# Replace 'elements' with the desired final key name
# xlsx_to_nested_json('input.xlsx', 'output.json', 'Sheet1', ['affiliations'], 'elements')
xlsx_to_nested_json(path_read, path_write, sheet_name, ['affiliations','interaction-participant-all', 'interaction-participant-leadership','interaction-participant-presenter','projects'],final_key)






data_elements = data_elements.replace('\[\]','',regex=True)

timestr = time.strftime("%Y%m%d-%H%M%S")
fname = '/Users/cgouldvanpraag/Desktop/kumu-data-json-elements_' + timestr + '.json'




data_elements.to_json(fname,orient="records")

with open(fname, 'r') as f:
  data = json.load(f)


# for key, value in data.items():
#         if value.str.contains('\|'):
#             # Override 'transactions' key with the single value that was generated from the first loop
#             # Initialize empty List
#             jsonFileContent["transactions"] = []
#             # Add Transaction to list
#             jsonFileContent["transactions"].append(transaction)
#         else:
#             # Write key value pair to a temporary object
#             jsonFileContent[key] = value
            
#     # Write all contents to file a file 'transactionTypeName'.json (e.g. 'can.json')
#     fileWrite = open(jsonFileContent['transactions'][0]['transactionTypeName']+'.json', 'w')
#     json.dump(jsonFileContent, fileWrite)               
#     fileWrite.close()


data_elements['interaction-participant-all'] = np.where(data_elements['interaction-participant-all'].str.contains('\|'),'["' + data_elements['interaction-participant-all'] + '"]' , data_elements['interaction-participant-all'])
data_elements['interaction-participant-all'] = data_elements['interaction-participant-all'].str.replace('|','","')

data_elements_json['interaction-participant-active'] = np.where(data_elements_json['interaction-participant-active'].str.contains('\|'),'["' + data_elements_json['interaction-participant-active'] + '"]' , data_elements_json['interaction-participant-active'])
data_elements_json['interaction-participant-active'] = data_elements_json['interaction-participant-active'].str.replace('|','","')

data_elements_json['interaction-participant-leadership'] = np.where(data_elements_json['interaction-participant-leadership'].str.contains('\|'),'["' + data_elements_json['interaction-participant-leadership'] + '"]' , data_elements_json['interaction-participant-leadership'])
data_elements_json['interaction-participant-leadership'] = data_elements_json['interaction-participant-leadership'].str.replace('|','","')

data_elements_json['interaction-participant-presenter'] = np.where(data_elements_json['interaction-participant-presenter'].str.contains('\|'),'["' + data_elements_json['interaction-participant-presenter'] + '"]' , data_elements_json['interaction-participant-presenter'])
data_elements_json['interaction-participant-presenter'] = data_elements_json['interaction-participant-presenter'].str.replace('|','","')

data_elements_json['affiliations'] = np.where(data_elements_json['affiliations'].str.contains('\|'),'["' + data_elements_json['affiliations'] + '"]' , data_elements_json['affiliations'])
data_elements_json['affiliations'] = data_elements_json['affiliations'].str.replace('|','","')

data_elements_json['projects'] = np.where(data_elements_json['projects'].str.contains('\|'),'["' + data_elements_json['projects'] + '"]' , data_elements_json['affiliations'])
data_elements_json['projects'] = data_elements_json['projects'].str.replace('|','","')

# # def df_to_nested_json_elements(df, key='elements'):
# #     result = {key: df.to_dict(orient='records')}
# #     return result

# # nested_json = df_to_nested_json_elements(data_elements_json)
# # # json.dumps(nested_json)

# timestr = time.strftime("%Y%m%d-%H%M%S")
# fname = '/Users/cgouldvanpraag/Desktop/kumu-data-json-elements_' + timestr + '.json'

# with open(fname, "w") as outfile:
#     outfile.write(nested_json)


# f = open(fname, "w")
# for row in data_elements_json.iterrows():
#     row[1].to_json(f)
#     f.write(",\n")

# data_elements.to_json(r'/Users/cgouldvanpraag/Library/CloudStorage/OneDrive-TheAlanTuringInstitute/E&S Grand Challenge - Documents/WS1 Ecosystem/stakeholder-mapping/data-sources/sharepoint-list-downloads/kumu-data-es-processed-20240220-elements.json', orient='values')
data_elements_json.to_json(r'/Users/cgouldvanpraag/Library/CloudStorage/OneDrive-TheAlanTuringInstitute/E&S Grand Challenge - Documents/WS1 Ecosystem/stakeholder-mapping/data-sources/sharepoint-list-downloads/kumu-data-es-processed-20240220-elements.json',orient="records")


# f = open("/Users/cgouldvanpraag/Desktop/kumu-data.json", "w")
# for row in data_elements_json.iterrows():
#     row[1].to_json(f)
#     f.write(",\n")


data_connections_json['to'] = np.where(data_connections_json['to'].str.contains('\|'),'["' + data_connections_json['to'] + '"]' , data_connections_json['to'])
data_connections_json['to'] = data_connections_json['to'].str.replace('|','","')


data_connections_json.reset_index(drop=True, inplace=True)
data_connections_json.to_json(r'/Users/cgouldvanpraag/Library/CloudStorage/OneDrive-TheAlanTuringInstitute/E&S Grand Challenge - Documents/WS1 Ecosystem/stakeholder-mapping/data-sources/sharepoint-list-downloads/kumu-data-es-processed-20240220-connections.json',orient="records")

# manually:
# copy paste from pretty-print view into "elements":[ ] and "connections":[ ]
# replace "[]" with ""
# replace \" with "
# replace "[" with ["
# replace "]" with "]
# Get rid of extra " (mostly in the notes column, some labels) which are messing up the syntax. Look for errors in JSON parsing (firefox)
# Get rid of "[]",



# #################


# %%%%%%%%%%%%%%%%%%%%%%%%%%%
# Kumu display settings: 2024-02-20

# @controls {
#   top-left {
#     search {}

#     filter {
#       target: element;
#       by: "type-what";
#       as: dropdown;
#       multiple: true;
#       default: show-all;
#       label: "filter by type";
#     }

#     showcase {
#       target: element;
#       by: "interaction-participant-all";
#       as: dropdown;
#       multiple: true;
#       default: select-none;
#       mode: normal;
#       label: "showcase by interaction-participant-all";
#     }

#     showcase {
#       target: element;
#       by: "countr";
#       as: dropdown;
#       multiple: true;
#       default: show-all;
#       mode: normal;
#       label: "showcase by country";
#     }
#   }
# }

# @settings {
#   template: stakeholder;
#   element-shape: categorize("type-what");
#   element-scale: scale("size", 0.5, 3);
#   element-color: categorize("type-what", Paired-inverted);
# }










# # %%%%%%%%%%%%%%%%%%%%%%%%%%%



