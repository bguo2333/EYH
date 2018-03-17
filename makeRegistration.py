import numpy as np
import os
import pandas as pd
import sys
import matplotlib.pyplot as plt



dat = pd.read_csv('Registration2018.csv')
dat.drop(['Timestamp', 'Email Address', 'Parent ', 'ParentNumber', 'ParentEmail', 'School', 'Grade', 'PreviousEYH', 'YearEYH', 'Marketing', 'Shirt', 'Access', 'Allergies', 'Payment', 'WhyWaiver', 'Photorelease', 'Waiver'], axis=1, inplace=True)


nTracks = 8
maxGirls = 11
tracks = { "Track %i"%(x+1):{'a':[], 'b':[], 'c':[]} for x in range(nTracks)}
full = { "Track %i"%(x+1):False for x in range(nTracks)}
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

for index, row in dat.iterrows():
	
	if not full['Track 4'] and ("Track 4" in row['FirstChoice'] or 'Track 4' in row['SecondChoice'] or 'Track 4' in row['ThirdChoice']):
		ideal = "Track 4"
	elif not full['Track 6'] and ("Track 6" in row['FirstChoice'] or 'Track 6' in row['SecondChoice'] or 'Track 6' in row['ThirdChoice']):
		ideal = "Track 6"
	elif not full[row['FirstChoice']]:
		ideal = row["FirstChoice"]	
	elif not full[row['SecondChoice']]:
		ideal = row['SecondChoice']
1	elif not full[row['ThirdChoice']]:
		ideal = row['ThirdChoice']
	else:
		ideal = 'NOMATCH'
	

	if ideal == "NOMATCH":
		unmatched.append(row['FirstName']+ " " + row['LastName'])
		continue

	smallest = min( tracks[ideal], key=lambda k: len(tracks[ideal][k]))
	tracks[ideal][smallest].append(row['LastName']+ ", " + row['FirstName'] + " \n")
	
	if len(tracks[ideal]['a']) == len(tracks[ideal]['b']) == len(tracks[ideal]['c']) == maxGirls:
		full[ideal] = True

####################

print 
print

print "Unmatched girls " + str(len(unmatched))
print unmatched
print


rots = [ ['a','b','c'],
	 ['b','c','a'],
	 ['c','a','b']]



 
for track in tracks:
	print track
	for i in xrange(3):
		csv_name = "leaderRosters/" + workshops[track][i] + ".csv"
		csv = open(csv_name, "w")
		title = "Last Name, First Name \n"
		csv.write(title)

		for rot in rots[i]:
			csv.write(" , \n")
			for name in tracks[track][rot]:
				csv.write(name)
