#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rajiv Srinath
DS 2000: Intro to Programming with Data
HW 7: bluebikes.py
Mon Oct 31 19:45:41 2022

Description: utilizes station.csv and trip.csv data in order to interpret trips and calculate, plot, and display important data
    
Output:
    Number of trips ending at Forsyth St at Huntington Ave:
    Sunday: 219
    Monday: 250
    Tuesday: 314
    Wednesday: 296
    Thursday: 277
    Friday: 481
    Saturday: 230

"""
import matplotlib.pyplot as plt
import math

EARTH_RADIUS = 3959

def read_trips_to_dict(filename, delimiter = ','):
    """ reads trips csv to a list of dictionaries
        parameters: filename (string - name of file)
                    delimiter - field delimiter (',')
        return: a table of data as a list of dictionaries
    """
    # Creates list for trips dictionaries
    trips_data = []
    
    # Opens and reads file =
    with open(filename, 'r') as infile:
        
        # read the header
        header = infile.readline().strip().split(delimiter)
            
        # Read remaining lines
        for line in infile:
            trips_dict = {}
            
            # parse values
            vals = line.strip().split(delimiter)
            
            # Store key value pairs

            for i in range(len(vals)):
                key = header[i]
                value = vals[i]
                trips_dict[key] = value
                
            trips_data.append(trips_dict) # add row to data
    
    return trips_data  

def read_stations_to_dict(filename, delimiter = ','):
    """ reads stations csv to stations dictionary
        parameters: filename (string - name of file)
                   delimiter = field delimiter (',')
        return: dictionary for stations values
    """
    # Creates dictionary for stations data
    stations_dict = {}
    
    # Opens and reads file
    with open(filename, 'r') as infile:
        
        # read the header
        header = infile.readline()
        
        # read the remaining line
        for line in infile:
            coordinates = []
            
            vals = line.strip().split(delimiter)
            
            # assigns values coordinates list
            coordinates.append(vals[1])
            coordinates.append(vals[2])
            
            stations_dict[vals[0]] = coordinates
           
    return stations_dict

def distance_and_time(trips_data, stations_data):
    """ calculates distance and speed for all trips 
        parameters: trips_data (list of dictionaries)
                    stations_data (dictionary)
        return: updated trip_data with distance and speed data
    """
    # parses through each trip in trips_data
    for trip in trips_data:
       # assigns start station, end station, and trip time to variables
       start = trip['start_station']
       end = trip['end_station']
       time = float(trip['duration']) / 3600
       
       # calculates and appends distance and speed to trip_data
       if start in stations_data and end in stations_data:
           lat1 = stations_data[start][0]
           long1 = stations_data[start][1]
           lat2 = stations_data[end][0]
           long2 = stations_data[end][1]
           
           lat1 = math.radians(float(lat1))
           long1 = math.radians(float(long1))
           lat2 = math.radians(float(lat2))
           long2 = math.radians(float(long2))
           
           delta_lat = lat2 - lat1
           delta_long = long2 - long1
           
           # the earth's radius is a constant value
           a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_long / 2)**2
           
           haversine = EARTH_RADIUS * 2 * math.asin(math.sqrt(a))
           
           trip['dist'] = haversine
           trip['mph'] = haversine/time
       
       # appends 'None' value if station is not in stations_data 
       else:
           trip['dist'] = 'None'
           trip['mph'] = 'None'
   
    return trips_data

def get_column(trips_data):
    """creates lists for distance and speed values
       parameters: trips_data (list of dictionaries)
       return: distance_list, speed_list
    """
    # creates lists for distances and speeds
    distance_list = []
    speed_list = []
    
    # parses through trips
    for trip in trips_data:
        
        # skips trip if distance or speed value is 'None'
        if trip['dist'] == 'None' or trip['mph'] == 'None':
            pass
        # appends distance and speed values to lists
        else:
            distance_list.append(trip['dist'])
            speed_list.append(trip['mph'])
    
    return distance_list, speed_list
        

def visualize_distribution(distance_list, speed_list):
    """creates histograms for distances and speeds for trips
       parameters: distance_list (list of strings)
                   speed_list (list of strings)
       return: none
       output: histogram for distances, histogram for speeds
    """
    # creates and displays distance histogram and assigns axis labels and title
    plt.hist(distance_list, bins = 100)
    plt.title("Distribution of Trip Distances")
    plt.xlabel("Trip Distances (km)")
    plt.ylabel("Frequency")
    plt.savefig('distances.pdf')
    plt.show()
    
    # creates and displays speed histogram and assigns axis labels and title
    plt.hist(speed_list, bins = 100, label = "Speeds (mph)")
    plt.title("Distribution of Trip Speeds")
    plt.xlabel("Trip Speeds (mph)")
    plt.ylabel("Frequency")
    plt.savefig('speeds.pdf')
    plt.show()

def new_dict(trips_data, stations_data):
    """creates and prints dictionary of number of trips ending at Forsyth St at Huntington Ave by day of the week
       parameters: trips_data (list of dictionaries)
                   stations_data (dictionary)
       return: none
       output: prints dictionary of number of trips by day of the week
    """
    # creates dictionary for number of trips by the day of the week
    days_dict = {}
    # creates list for days of the week
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    
    # assigns starting count (0) for each key of day of the week
    for day in days:
        days_dict[day] = 0
    
    # parses through each trip in trips_data
    for trip in trips_data:
        # checks if trip ends at specific station
        if trip['end_station'] == 'Forsyth St at Huntington Ave':
            # parses through days of the week
            for day in days:
                # increments count for day of the week of trip
                if trip['start_day_name'] == day:
                    days_dict[day] += 1
        else:
            pass
    
    # prints report of dictionary of trips on each day of the week
    print("Number of trips ending at Forsyth St at Huntington Ave:")
    
    for day in days:
        print(f"{day}: {days_dict[day]}")
    
    
def main():
    # reads trips.csv and stations.csv and assigns return values to variables
    trips_data = read_trips_to_dict("trips.csv")
    stations_data = read_stations_to_dict("stations.csv")
    
    # calls distance_and_time function in order to update trips_data 
    distance_and_time(trips_data, stations_data)
    
    # calls get_column function to create lists for distances and speeds
    distance_list, speed_list = get_column(trips_data)
    
    # calls visualize_distribution function in order to create histograms
    visualize_distribution(distance_list, speed_list)
    
    # calls new_dict function to create and display dictionary of trip counts by day of the week
    new_dict(trips_data, stations_data)
    


if __name__ == "__main__":
    main()

