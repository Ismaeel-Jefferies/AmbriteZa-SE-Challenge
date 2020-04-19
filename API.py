#Author: Ismaeel Jefferies
#Date: 2020-04-19
#Summary: An API for for the viewing of latitude and longitude coordinates of an ipv4 address, posed by AmbriteZa as a Software Engineering Challenge


import flask
from flask import request, jsonify
import json
from math import*

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Software Engineer Interview Challenge</h1>
<p>An API for for the viewing of latitude and longitude coordinates of an ipv4 address.</p>'''

#=================================================================================================================#

## Importing the files to be used

#importing the data.json file
with open('C:/Users/Ismaeel/projects/_API/data.json') as f:
  data = json.load(f)

#data keys = dict_keys(['active', 'asn', 'countrycode', 'id', 'statecode', 'meta'])

#importing the geo.json file
with open('C:/Users/Ismaeel/projects/_API/geo.json') as f:
  geo = json.load(f)

#geo keys = dict_keys(['ipv4', 'geo'])

#=================================================================================================================#

## First: validity checks

#geo JSON file check:
# ipv4 value should have four sets of numbers in the range [0,255] and separated by a decimal point '.'
# geo value should have two sets of numbers separated by a comma

def ipv4_check(ipv4):
	index = 0
	dot_index = list()

	#places the index of a dot in a list for later reference
	for item in ipv4:
		if item == ".":
			dot_index.append(index)
		index += 1
	
	#checks if there are not only 3 dots in the ipv4 address
	if len(dot_index) < 3 or len(dot_index) > 3:
		print("Invalid ipv4")
		return False

	#these are the numbers inbetween the dots
	num1 = int(ipv4[0:dot_index[0]])
	num2 = int(ipv4[(dot_index[0]+1):dot_index[1]])
	num3 = int(ipv4[(dot_index[1]+1):dot_index[2]])
	num4 = int(ipv4[(dot_index[2]+1):])

	#checks if the above numbers are within the range of [0,255]
	if (num1 < 0 or num1 > 255) or (num2 < 0 or num1 > 255) or (num3 < 0 or num1 > 255) or (num4 < 0 or num1 > 255):
		print("Invalid ipv4 address")
		return False
	
	 #if valid ipv4 address
	return True


def geo_check(G_YO): #string parameter ideally comprising of a comma separating two floats
	comma_index = G_YO.find(",") # returns -1 if no comma is found
	if comma_index != -1:
		return True

	print("Invalid geo value")
	return False

@app.route('/geoValidate', methods=['GET']) #e.g http://127.0.0.1:5000/geoValidate
# geo JSON file validation
#---------------------------------------------------------------------------------------------------------#
def geo_validate():																						  
	Flag = True																							  
																										  
	for index in range(len(geo)):																		  
		ipv4 = geo[index]["ipv4"]																		  
		G_YO = geo[index]["geo"]																		  
																										  
		if ipv4_check(ipv4) == False or geo_check(G_YO) == False:										  
			Flag = False																				  
			print("Invalid geo data : "+str(geo[index])+" at index "+str(index)+" of the geo JSON file")  
																										  
	return "The geo JSON file is valid"																      
#---------------------------------------------------------------------------------------------------------#

# data JSON file check
# 'active' should have an int value
# 'asn' should have an int value  
# 'countrycode' should have a string value
# 'id' should have an int value
# 'meta' should have a string value

@app.route('/dataValidate', methods=['GET']) #e.g http://127.0.0.1:5000/dataValidate
# data JSON file validation
#------------------------------------------------------------------------------------------------------------------------------------#
def data_validate():																												 
	Flag = True																														 
																																	 
	for index in range(len(data)):																									 
		active = data[index]["active"]																								 
		asn = data[index]["asn"]																									 
		countrycode = data[index]["countrycode"]																					 
		Id = data[index]["id"]																										 
		meta = data[index]["meta"]																									 
																																	 
		if (type(active) != int) or (type(asn) != int) or (type(countrycode) != str) or (type(Id) != int) or (type(meta) != str):	 
			Flag = False																											 
			print("Invalid data : "+str(data[index])+" at index "+str(index)+" of the data JSON file")								 
																																	 
	return "The data JSON file is valid"																							 
#------------------------------------------------------------------------------------------------------------------------------------#


#=================================================================================================================#

# Second: Euclidean distance sorting

#this a function that checks that all of the ipv4 addresses in the geo JSON file are present in the data JSON file
def checkIf_ipv4sAre_presentIn_data():
	checks = list()

	for i in range(len(geo)):
		for j in range(len(data)):
			#the ipv4 address should be contained in the meta key in the data Json file
			if geo[i]['ipv4'] in data[j]['meta']:
				checks.append('True')
				break

	count = 0

	for i in checks:
		if i == 'True':
			count += 1

	if count == len(checks):
		print("All of the ipv4 addresses in the geo JSON file are present in the data JSON file")
	else:
		print("All of the ipv4 addresses in the geo JSON file are NOT present in the data JSON file")

#(remove # to check)checkIf_ipv4sAre_presentIn_data()

def euclidean_distance(x1,y1,x2,y2):
	return sqrt((x2-x1)**2 + (y2-y1)**2)

#this function is to be used by the methods employed by the API. Its core function is sorting the data.json by euclidean distance from the latitude and longitude
def sort_dataFile_by_euclideanDistance(latitude,longitude):								  	                																			    #
	dataSort = data.copy()																 	
	geo_euc = geo.copy()																  	
																						  	
	for i in range(len(geo_euc)):														  	
		#find the index of the comma separating the latitude and longitude in the geo data  
		comma_index = geo_euc[i]['geo'].find(',')										  	
		lat = float(geo_euc[i]['geo'][0: comma_index])									  	
		lon = float(geo_euc[i]['geo'][(comma_index+1):])                                  	
		                                 												  				
		euc_dist = euclidean_distance(lat,lon,latitude,longitude)            			    
		#creating a new euclidean distance key in the geo data for later reference          
		geo_euc[i]['euclidean distance'] = euc_dist 									  	
																						  	
	for j in range(len(dataSort)):														  	
		if geo_euc[j]['ipv4'] in dataSort[j]['meta']:									  	
			dataSort[j]['euclidean distance'] = geo_euc[j]['euclidean distance']		  	
																						  	
	#sorts data in increasing euclidean distances from the entered latitude and longitude 	
	return sorted(dataSort, key = lambda i: i['euclidean distance'])

@app.route('/sortData', methods=['GET']) #e.g http://127.0.0.1:5000/sortData?latitude=100&longitude=100
#data.json sorted by euclidean distance from the latitude and longitude
#-----------------------------------------------------------------------------------------------#
def sort_Euclid():								  	                							
	if 'latitude' and 'longitude' in request.args:                                          	
		latitude = float(request.args['latitude'])                                          	
		longitude = float(request.args['longitude'])                                        	
	else:                                                                                   	
		return "Error: latitude or longitude fields not provided. Please specify coordinates."  
																						    	
	#sorts data in increasing euclidean distances from the entered latitude and longitude 		
	return jsonify(sort_dataFile_by_euclideanDistance(latitude,longitude)) 						
#-----------------------------------------------------------------------------------------------#


#=================================================================================================================#

# Third: returns the row from data.json with the shortest distance from the latitude and longitude

@app.route('/shortestRow', methods=['GET']) #e.g http://127.0.0.1:5000/shortestRow?latitude=100&longitude=100
#----------------------------------------------------------------------------------------------------------------------------------------#
def shortest_row():																														 
	if 'latitude' and 'longitude' in request.args:                                          											 
		latitude = float(request.args['latitude'])                                          											 
		longitude = float(request.args['longitude'])                                        											 
	else:                                                                                   											 
		return "Error: latitude or longitude fields not provided. Please specify coordinates."                                           
																											                             
	shortest_distance_row = sort_dataFile_by_euclideanDistance(latitude,longitude)[0]												     
																																		 
	print("The row from data.json with the shortest distance from the latitude = {0} and longitude = {1} :".format(latitude,longitude))  
																																		 
	return jsonify(shortest_distance_row)																				                 
#----------------------------------------------------------------------------------------------------------------------------------------

app.run()