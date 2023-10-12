## Syllabus to ID-Name dict
## By:  Irfan Nurhadi Satria
## Date: 2023/09/21
## Purpose: this script purpose is to parse the syllabus files and generate a new JSON that maps course IDs to 
## Course Names for further treatment

import json

# Open the syllabus file
## NOTE: put the syllabus file in the syllabus_files directory
with open('syllabus_files/SILS.json', 'r') as f:
    syllabus = json.load(f)

# Create a new dict
result = {}
for course in syllabus:
    id = course['a']
    name = course['b']
    result.update({id: name})

# Write the result to a new JSON file
with open('syllabus_files/syllabus_id_name.json', 'w') as f:
    json.dump(result, f, indent=4)

print('Done!')