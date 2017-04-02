import pandas as pd
import numpy as np
from pylab import *
import matplotlib
import matplotlib.pyplot as plt
import collections
from matplotlib.backends.backend_pdf import PdfPages
import textwrap
import os
import sys


def getFracs(toFrac):
    
    final = {}
        
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

		fracs = getFracs(toFrac)


		with PdfPages(outdir + workshop + ".pdf") as pp:

			plt.rcParams["axes.titlesize"] = 10
			plt.rcParams['font.size'] = 8
			plt.rcParams['figure.figsize'] = 8.5, 11
			plt.rcParams['text.color'] = 'w'
			plt.suptitle(workshop,fontsize=20,color='k',wrap=True)

			
			ax1 = plt.subplot2grid((3,2),(0, 0))
			ax2 = plt.subplot2grid((3,2),(0, 1))
			ax3 = plt.subplot2grid((3,2),(1, 0))
			ax4 = plt.subplot2grid((3,2),(1, 1))
			ax5 = plt.subplot2grid((3,2),(2, 0))
			ax6 = plt.subplot2grid((3,2),(2, 1))




			# fig, axes = plt.subplots(3, 2, sharex=True, sharey=True)


			# for question, axis in zip(fracs,axes):
			# 	print question
			# 	axis.pie(fracs[question].values(),autopct='%1.1f%%')
			# 	axis.set_title(question,wrap=True)
			# 	plt.legend(evals.values(),loc="best")

			#this should be in a loop but I cant for the life of me figure out how

			question = "I felt comfortable asking questions at the workshop."
			ax1.pie(fracs[question].values(),autopct='%1.1f%%')
			ax1.set_title("I felt comfortable asking \n questions at the workshop.", fontsize=11,color='k')
			ax1.axis('equal')
			#plt.legend(evals.values(),loc="best")

			question = "I enjoyed the workshop and learned something interesting."
			ax2.pie(fracs[question].values(),autopct='%1.1f%%')
			ax2.set_title("I enjoyed the workshop and \n learned something interesting.", fontsize=11,color='k')
			ax2.axis('equal')
			#plt.legend(evals.values(),loc="best")

			question = "I think I would enjoy the workshop leaders' job."
			ax3.pie(fracs[question].values(),autopct='%1.1f%%')
			#ax3.set_title("I think I would enjoy the \n workshop leaders' job.")
			ax3.set_title("I think I would enjoy the workshop leaders' job.", fontsize=11,color='k')
			ax3.axis('equal')
			#plt.legend(evals.values(),loc="best")

			question = "The workshop made me feel like I can have a job in science, engineering or math."
			ax4.pie(fracs[question].values(),autopct='%1.1f%%')
			ax4.set_title("The workshop made me feel like I can \n have a job in science, engineering or math.",fontsize=11,color='k')
			ax4.axis('equal')
			#plt.legend(evals.values(),loc="best")

			question = "I enjoyed listening to my workshop leader give their presentation."
			ax5.pie(fracs[question].values(),autopct='%1.1f%%')
			ax5.set_title("I enjoyed listening to my workshop \n leader give their presentation.",fontsize=11,color='k')
			ax5.axis('equal')
			#plt.legend(evals.values(),loc="best"

			plt.rcParams['text.color'] = 'k'
			pie = ax6.pie([1,1,1,1,1], labels=evals.values())
			l = ax6.legend(loc="center",prop={'size':14})
			ax6.axis('equal')
			for group in pie:
				for x in group:
					x.set_visible(False)



			pp.savefig()
			plt.close()


			fig = plt.figure()

			plt.rcParams["axes.titlesize"] = 10
			plt.rcParams['font.size'] = 8
			plt.rcParams['figure.figsize'] = 8.5, 11
			plt.suptitle('Comments',fontsize=20)


			#out_comments = formatComments(Comments)
			x_init = 0
			y_init = 1.08
			x = x_init
			y = y_init
			plt.axis('off')
			for comment in Comments:
				if len(comment):
					y -= .08
					plt.text(x ,y ,comment, horizontalalignment='left',verticalalignment='top', fontsize=12, wrap=True,color='k')

			pp.savefig()
			plt.close()




