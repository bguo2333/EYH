import pandas as pd
import numpy as np
from pylab import *
import collections
import os
import sys


def getFracs(toFrac):
    
    final = {}
    
    len(toFrac)
        
    for question in toFrac:
        fracs={}
        questioninfo = toFrac[question]
        total = len(questioninfo)
        
        counter = collections.Counter(questioninfo)
                
        for key in counter.keys():
            ind = counter.keys().index(key)
            fracs[key] = round(float(counter.values()[ind])/total * 100,1)
        
        
        final[question] = fracs
        
        
    
    return final



if __name__ == '__main__':
	
	dat = pd.read_csv('WorkshopEvals2.csv')
	dat.fillna('', inplace=True)
	dat.drop('Timestamp',axis=1,inplace=True)
	
	workshops = list(set(dat['Workshop'].values))
	
	evals = {5:"Strongly Agree", 4:"Agree", 3:"Neutral", 2:"Disagree", 1:"Strongly Disagree"}
	outdir = './evaluations/'



	for workshop in workshops:
		r_Questions = dat[dat["Workshop"] == workshop].Questions
    	r_Learned = dat[dat["Workshop"] == workshop].Learned
    	r_LeadersJob = dat[dat["Workshop"] == workshop].LeadersJob
    	r_JobInStem = dat[dat["Workshop"] == workshop].JobInStem
    	r_Presentation = dat[dat["Workshop"] == workshop].Presentation
    	Comments = dat[dat["Workshop"] == workshop].Comments
    
    	toFrac = {"I felt comfortable asking questions at the workshop.":r_Questions, "I enjoyed the workshop and learned something interesting.":r_Learned,
              "I think I would enjoy the workshop leaders' job.":r_LeadersJob, "The workshop made me feel like I can have a job in science, engineering or math.":r_JobInStem,
              "I enjoyed listening to my workshop leader give their presentation.":r_Presentation}
    
    	tot = len(r_Questions)


    	output = open(outdir +workshop + '.pdf',"w")
    	Comments = filter(None,Comments) #only print non empty values
    	output.write(workshop + "\n \n")
    	output.write("Comments: \n")
    	for comment in Comments:
    		output.write(comment + "\n")

    	print workshop

    	fracs = getFracs(toFrac)

    	for question in fracs:
    		print question
    		figure(1, figsize=(6,6))
    		ax = axes([0.1, 0.1, 0.8, 0.8])
    		pie(fracs[question].values(),labels=fracs[question].values(),autopct='%1.1f%%')
    		title(question)
    		show()





