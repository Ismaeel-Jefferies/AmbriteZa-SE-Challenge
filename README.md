# AmbriteZa-SE-Challenge
Here is the task: Write a flask backend API (no frontend needed, simple REST or POST requests) to perform the following tasks:
1. Write a function that performs some validity checks on a JSON file, use geo.json and data.json as input.

2. Write a function that takes in latitude and longitude as parameters, and returns the data from data.json sorted by euclidean distance from the latitude longitude.

3. Write a function that takes in latitude and longitude as parameters, and returns the row from data.json with the shortest distance from the latitude and longitude, in a nicely formatted way.

Download the API.py script, data.json and geo.json files to your computer

At lines 24: "with open('C:/Users/Ismaeel/projects/_API/data.json') as f:"
and 30: "with open('C:/Users/Ismaeel/projects/_API/geo.json')", replace "C:/Users/Ismaeel/projects/_API/" with the path on your
computer to these json files

Navigate to the location of API.py on your computer through the command prompt and execute it via the following command: python API.py

To test the output of task 1, visit http://127.0.0.1:5000/geoValidate and http://127.0.0.1:5000/dataValidate after running the API.py script.

To test the ouput of task 2, visit http://127.0.0.1:5000/sortData?latitude=100&longitude=100 , to change the latitude and longitude values simply change them after the '=' sign as shown above.

To test the ouput of task 3, visit http://127.0.0.1:5000/shortestRow?latitude=100&longitude=100 , to change the latitude and longitude values simply change them after the '=' sign as shown above.
