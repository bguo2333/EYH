import pandas as pd
import numpy as np
import os
import sys

if __name__ == '__main__':
    dat = pd.read_csv('EYH_Registration_2017.csv')

    dat.drop(['timestamp', 'E-mail address', 'Payment received', 'waiver received', 'PHOTORELEASE', 'School', 'Grade',
              'Have you previously attended EYH?', 'If so, which year(s) have you attended?',
              'T-shirt size (adult sizes)', 'Do you have any accessibility needs?', 'Do you have any allergies?',
              'Payment type', 'Why are you requesting a scholarship', 'Please select your top 3 workshops.'], axis=1,
             inplace=True)

    tracks = list(set(dat['track'].values))
    subtracks = list(set(dat['subtrack']))

    dat['student_id'] = np.arange(len(dat))

    for track in tracks:
        for subtrack in subtracks:
            cond = (dat['track'] == track) & (dat['subtrack'] == subtrack)

            names = pd.DataFrame(data=np.array([dat[cond]['First name'], dat[cond]['Last name']]).T,
                                 columns=['First Name', 'Last_Name'])

            names.to_csv(('Rosters_for_buddies/%02d_' + subtrack + '.csv') % track, index=False)

    rotations1 = [['a', 'b', 'c'],
                  ['g', 'e', 'i'],
                  ['d', 'h', 'f']]

    rotations2 = [['d', 'e', 'f'],
                  ['a', 'h', 'c'],
                  ['g', 'b', 'i']]

    rotations3 = [['g', 'h', 'i'],
                  ['d', 'b', 'f'],
                  ['a', 'e', 'c']]

    rotations = [rotations1, rotations2, rotations3]
    workshops = set(dat['1st workshop'].values)

    for workshop in workshops:
        count = 1
        track = list(set(dat[dat['1st workshop'] == workshop].track))[0]
        cat = sorted(list(set(dat[dat['1st workshop'] == workshop].subtrack)))[0]

        possible_students = dat[dat.track == track].student_id.values
        student_subtracks = dat[dat.track == track].subtrack.values

        named_rosters_path = './named_rosters_for_workshops/'
        if not os.path.exists(named_rosters_path): os.mkdir(named_rosters_path)

        for rotation in rotations:
            if cat in rotation[0]:
                for rot in rotation:
                    roster = np.array(
                        [possible_students[i] for i in xrange(len(possible_students)) if student_subtracks[i] in rot])
                    named_roster = []
                    for value in roster:
                        named_roster.append([dat[dat.student_id == value]['First name'].values[0],
                                             dat[dat.student_id == value]['Last name'].values[0]])
                    named_roster = np.array(named_roster)

                    named_roster_df = pd.DataFrame(named_roster, columns = ['First Name', 'Last Name'])
                    workshop = workshop.replace(' ', '_')
                    named_roster_df.to_csv(os.path.join(named_rosters_path, workshop + '_%02d.csv'%count), index = False)
                    count += 1

