import numpy as np
import os
import pandas as pd
import sys
import matplotlib.pyplot as plt



dat = pd.read_csv('Registration2018.csv')
dat = dat[['FirstName','LastName','FirstChoice','SecondChoice','ThirdChoice']]

buddy_df = pd.read_csv('2018Volunteers.csv')
buddy_df = buddy_df[['FirstName','LastName']]

#dat.drop(['Timestamp', 'Email Address', 'Parent ', 'ParentNumber', 'ParentEmail', 'School', 'Grade', 'PreviousEYH', 'YearEYH', 'Marketing', 'Shirt', 'Access', 'Allergies', 'Payment', 'WhyWaiver', 'Photorelease', 'Waiver'], axis=1, inplace=True)


nTracks = 8
maxGirls = 12
almostgirls = 11
girlBuddies = 6
tracks = { "Track %i"%(x+1):{1:[], 2:[], 3:[]} for x in range(nTracks)}
full = { "Track %i"%(x+1):False for x in range(nTracks)}
almostfull = { "Track %i"%(x+1):False for x in range(nTracks)}
choices = ['First','Second','Third']
unmatched = []

workshops = {
	"Track 1": ["Paleontology is Dino-mite", "Science is Delicious!", "Math and Dance"], 
	"Track 2": ["Coding With Robots!", "Sticky and Stretchy: Material Properties in Everyday Life", "Peeling of Banana DNA"], 
	"Track 3":["Private Eye: Zoom In On Nature", "Engineering an Exoskeleton", "Chocolate and the Speed of Light"], 
	"Track 4": ["Mapping the Future", "Saving Species with Feces", "Speak(er) Your Mind!"], 
	"Track 5": ["Microscopy For Everyone", "Webcomic Remix", "Viral Infection and How Your Body Fights Back"], 
	"Track 6": ["Hidden Signals", "deCODEing DNA", "Stitches Get Switches"], 
	"Track 7": ["Plantastic! The Wonderful World of Plants", "Made You Look!", "Escape Room: Code Your Way Out!"],
	"Track 8": ["Lucy and the 3D Printer", "Becoming a Natural with Natural Products", "Housing Hijinks"]}

print tracks

print len(dat)

########################
#print first choices
for choice in choices:

	print '%s Choice'%choice
	for q in range(nTracks):
		x = q+1
		print "Track " + str(x) + ": " + str((dat['%sChoice'%choice] == 'Track %i'%x).sum())
	print 

#######################
totalGirls = 0
girlsInTracks = 0

for index, row in dat.iterrows():

	print row
	
	if pd.isnull(row['FirstName']) :
		continue
		
	totalGirls += 1	
	
	if pd.isnull(row['FirstChoice']):
		ideal = "NOMATCH"
	elif not full[row['FirstChoice']] and not almostfull[row['FirstChoice']]:
		ideal = row["FirstChoice"]	
	elif not full[row['SecondChoice']] and not almostfull[row['SecondChoice']]:
		ideal = row['SecondChoice']
	elif not full[row['ThirdChoice']] and not almostfull[row['ThirdChoice']]:
		ideal = row['ThirdChoice']
	else:
		ideal = 'NOMATCH'
	

	if ideal == "NOMATCH":
		unmatched.append(row['FirstName']+ ", " + row['LastName'] + " \n")
		continue

	smallest = min( tracks[ideal], key=lambda k: len(tracks[ideal][k]))
	tracks[ideal][smallest].append(row['LastName']+ ", " + row['FirstName'] + " \n")
	
	if len(tracks[ideal][1]) == len(tracks[ideal][2]) == len(tracks[ideal][3]) == almostgirls:
		almostfull[ideal] = True
	if len(tracks[ideal][1]) == len(tracks[ideal][2]) == len(tracks[ideal][3]) == maxGirls:
		full[ideal] = True

print "printing unmatched"

#this big to do to make sure that everything is evenly distributed
for name in unmatched:
	print name
	found = False
	smalls = []
	for track in tracks:
		if not almostfull[track] and not found:
			smallest = min ( tracks[track], key=lambda k: len(tracks[track][k]))
			tracks[track][smallest].append(name)
			found = True
			if len(tracks[track][1]) == len(tracks[track][2]) == len(tracks[track][3]) == maxGirls:
				full[track] = True
			if len(tracks[track][1]) == len(tracks[track][2]) == len(tracks[track][3]) == almostgirls:
				almostfull[track] = True
			break
	if not found:
		for track in tracks:
			if not full[track] and not found:
				smallest = min ( tracks[track], key=lambda k: len(tracks[track][k]))
				tracks[track][smallest].append(name)
				found = True
				if len(tracks[track][1]) == len(tracks[track][2]) == len(tracks[track][3]) == maxGirls:
					full[track] = True
	if not found:
		print "ALERT"



#assign buddies, probably a smarter way to do this but I am tired



####################

print 
print

print "Unmatched girls " + str(len(unmatched))
print unmatched
print


rots = [ [1,2,3],
	 [2,3,1],
	 [3,2,1]]


#print tracks
 
for track in tracks:
	for x in xrange(3):
		csv_name = "Rosters/leaderRosters/" + workshops[track][x] + ".csv"
		csv = open(csv_name, "w")
		title = "Last Name, First Name, Buddy Name \n"
		csv.write(title)

		print "track " + track + " group " + str(x) + " with " +  str(len(tracks[track][x+1]))
		girlsInTracks += len(tracks[track][x+1])
		for rot in rots[x]:
			csv.write(" , \n")
			csv.write(" , \n")
			for name in tracks[track][rot]:
				csv.write(name)

print "total girls ", totalGirls
print "girls in tracks ", girlsInTracks

csv_name = "Rosters/Master.csv"
csv = open(csv_name,"w")
title = "Track, First Workshop, Last Name, First Name \n"
for track in tracks:
	for rot in tracks[track]:
		for name in tracks[track][rot]:
			row = track + " ," + workshops[track][rot-1] + " ," + name
			csv.write(row)




