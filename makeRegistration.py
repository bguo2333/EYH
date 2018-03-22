import numpy as np
import os
import pandas as pd
import sys
import matplotlib.pyplot as plt


def getBuddyName(name):
	for bud in partners:
		if name in partners[bud]["girls"]:
			buddyName = bud
	return buddyName




#girls registration
dat = pd.read_csv('Registration2018.csv')
dat = dat[['FirstName','LastName','FirstChoice','SecondChoice','ThirdChoice']]

#buddy registration
buddy_df = pd.read_csv('2018Volunteers.csv')
buddy_df = buddy_df[['FirstName','LastName']]

b = []
for index, row in buddy_df.iterrows():
	b.append(row['FirstName'] + " " + row['LastName'])

nTracks = 8
maxGirls = 12
almostgirls = 11
girlBuddies = 6

tracks = { "Track %i"%(x+1):{1:[], 2:[], 3:[]} for x in range(nTracks)}
buddies = { "Track %i"%(x+1):{1:[ b[6*x], b[6*x+1] ], 2:[ b[6*x+2], b[6*x+3] ], 3:[ b[6*x+4], b[6*x+5] ]} for x in range(nTracks)}
full = { "Track %i"%(x+1):False for x in range(nTracks)}
almostfull = { "Track %i"%(x+1):False for x in range(nTracks)}
dumb = ['a','b','c','d','e','f']




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

#put the girls into tracks
for index, row in dat.iterrows():

	
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
		unmatched.append(row['FirstName']+ ", " + row['LastName'])
		continue

	smallest = min( tracks[ideal], key=lambda k: len(tracks[ideal][k]))
	tracks[ideal][smallest].append(row['LastName']+ ", " + row['FirstName'])
	
	if len(tracks[ideal][1]) == len(tracks[ideal][2]) == len(tracks[ideal][3]) == almostgirls:
		almostfull[ideal] = True
	if len(tracks[ideal][1]) == len(tracks[ideal][2]) == len(tracks[ideal][3]) == maxGirls:
		full[ideal] = True


#this big to do to make sure that everything is evenly distributed, these girls who registered late are assigned at relative random, can maybe do this smarter
for name in unmatched:
	found = False
	smalls = []

	#fill all the ones that are not close to full first
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
	#then fill em up
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




####################


print "Unmatched girls " + str(len(unmatched))
print unmatched


rots = [ [1,2,3],
	 [2,3,1],
	 [3,2,1]]



#print tracks

partners={}

#make buddy assignments
for track in tracks:
	for x in xrange(3):
		partners[ buddies[track][x+1][0] ] = {"girls":tracks[track][x+1][0:5], "firstWorkshop": workshops[track][x], "secondWorkshop":workshops[track][rots[x][1]-1], "thirdWorkshop":workshops[track][rots[x][2] -1],"track": track, "id":str(track.strip("Track ")) + dumb[2*x]}
		partners[ buddies[track][x+1][1] ] = {"girls":tracks[track][x+1][5:], "firstWorkshop": workshops[track][x], "secondWorkshop": workshops[track][rots[x][1]-1 ], "thirdWorkshop":workshops[track][rots[x][2] -1 ], "track": track, "id":str(track.strip("Track "))+dumb[2*x+1]}
		


#rosters for leaders
for track in tracks:
	for x in xrange(3):
		csv_name = "Rosters/leaderRosters/" + workshops[track][x] + ".csv"
		csv = open(csv_name, "w")
		csv.write( workshops[track][x] + ", \n")
		csv.write(" , \n")
		title = "Last Name, First Name, Buddy Name, BuddyID \n"
		csv.write(title)
		
		print track + " group " + str(x) + " with " +  str(len(tracks[track][x+1]))
		girlsInTracks += len(tracks[track][x+1])
		
		
		for rot in rots[x]:
			csv.write(" , \n")
			csv.write(" , \n")
			for name in tracks[track][rot]:
				buddyName = getBuddyName(name)

				
				csv.write(name + " ," + buddyName + "," + partners[buddyName]["id"] + " \n")


print "total girls ", totalGirls
print "girls in tracks ", girlsInTracks



#list of buddies with track and workshops
csv_name = "Rosters/buddylist.csv"
csv = open(csv_name, "w")
title = "Buddy ID, Name, Track, First Workshop, Second Workshop, Third Workshop"
csv.write(title)
csv.write(" , \n")
for bud in partners:
	csv.write( partners[bud]["id"] + "," + bud +  " , " + partners[bud]["track"] + " ," + partners[bud]["firstWorkshop"] + "," + partners[bud]["secondWorkshop"] + "," + partners[bud]["thirdWorkshop"] + "\n")


#rosters for buddies
for bud in partners:
	csv_name = "Rosters/buddyRosters/" +partners[bud]["id"] + "_"+ bud + ".csv"
	csv = open(csv_name, "w")
	csv.write(partners[bud]["id"])
	csv.write(bud + ", \n")
	csv.write(" , \n")
	title = "Last Name, First Name \n"
	csv.write(title)
	csv.write(" , \n")
	csv.write( "Track: , "+ partners[bud]["track"] + " \n")
	csv.write( "First Workshop: , "+ partners[bud]["firstWorkshop"] + " \n")
	csv.write( "Second Workshop: , "+ partners[bud]["secondWorkshop"] + " \n")
	csv.write( "Third Workshop: , "+ partners[bud]["thirdWorkshop"] + " \n")
	csv.write(" , \n")
	for name in partners[bud]["girls"]:
		csv.write(name + " \n")



#master roster
csv_name = "Rosters/Master.csv"
csv = open(csv_name,"w")
title = "Track, Last Name, First Name, Buddy Name, Buddy ID, First Workshop, Second Workshop, Third Workshop \n"
csv.write(title)
for track in tracks:
	for rot in tracks[track]:
		for name in tracks[track][rot]:
			buddyName = getBuddyName(name)
			row = track + " ," + name + " ,"+ buddyName + ", " + partners[buddyName]["id"] + "," + partners[buddyName]["firstWorkshop"] + " , " + partners[buddyName]["secondWorkshop"] + " , "+partners[buddyName]["thirdWorkshop"]+" \n"
			csv.write(row)




