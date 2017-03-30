import numpy as np
import csv
# import science_plot_style.science_plot_style as sps
import science_plot_style_ as sps
import matplotlib.pyplot as plt
from pylab import *


def read_file(fn):
    data = []
    with open(fn) as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return np.array(data)


def get_fracs(nn, ws, data, wsn, wsd):
    q = wsd[:, nn]
    num_r = len(q)

    fracs = np.array([0, 0, 0, 0])
    for i in range(num_r):
        try:
            num = float(q[i])
            # print num
            fracs[num - 1] += 1
        except ValueError:
            print 'skipping'
    fracsC = fracs
    fracs = fracs[[0, 2, 1, 3]]
    ind = np.where(fracs > 0)
    return fracs, ind


def get_all_fracs(ws, data, wsn):
    ind = np.where(data[:, 1] == wsn[ws])
    num_r = len(ind[0])

    wsd = data[ind]

    fracsq1, ind1 = get_fracs(2, ws, data, wsn, wsd)
    fracsq2, ind2 = get_fracs(3, ws, data, wsn, wsd)
    fracsq3, ind3 = get_fracs(4, ws, data, wsn, wsd, )
    fracsq4, ind4 = get_fracs(5, ws, data, wsn, wsd)
    cmts = wsd[:, 6]

    return fracsq1, fracsq2, fracsq3, fracsq4, ind1, ind2, ind3, ind4, cmts


def make_autopct(values):
    def my_autopct(pct):
        # print 'pct', pct
        total = sum(values)
        val = int(round(pct * total / 100.0))
        if val > 2:
            return '{p:.0f}%  ({v:d})'.format(p=pct, v=val)
        else:
            return ''

    return my_autopct


if __name__ == '__main__':
    fn = "/Users/lisa/Dropbox/EYH_Evals/Workshop_evals/responses.csv"
    data = read_file(fn)

    wsn = list(set(data[:, 1][1:]))
    ws = 0
    q1 = []
    q2 = []
    q3 = []
    q4 = []
    for i in range(len(wsn)):
        ws = i
        fracsq1, fracsq2, fracsq3, fracsq4, ind1, ind2, ind3, ind4, cmts = get_all_fracs(ws, data, wsn)

        colors = np.array(['yellowgreen', 'lightskyblue', 'lightcoral', 'gold'])
        labels = np.array(['Strongly agree', 'Disagree', 'Agree', 'Strongly \ndisagree'])
        w = 215.9
        h = 310.4 - 40
        fig = sps.figure_in_mm(w, h + 30)
        ax = sps.axes_in_mm(0, 0, w, h)
        ss = 65
        mw = 25.4
        ax1 = sps.axes_in_mm(mw, h - mw - ss, ss, ss)
        plt.pie(fracsq1[ind1], labels=labels[ind1], colors=colors[ind1], autopct=make_autopct(fracsq1[ind1]),
                shadow=True)  # startangle=90)

        ax2 = sps.axes_in_mm(2.5 * mw + ss, h - mw - ss, ss, ss)
        plt.pie(fracsq2[ind2], labels=labels[ind2], colors=colors[ind2], autopct=make_autopct(fracsq2[ind2]),
                shadow=True)  # , startangle=90)

        ax3 = sps.axes_in_mm(mw, h - (2. * mw + ss) - ss, ss, ss)
        plt.pie(fracsq3[ind3], labels=labels[ind3], colors=colors[ind3], autopct=make_autopct(fracsq3[ind3]),
                shadow=True)  # , startangle=90)

        ax4 = sps.axes_in_mm(2.5 * mw + ss, h - (2. * mw + ss) - ss, ss, ss)
        plt.pie(fracsq4[ind4], labels=labels[ind4], colors=colors[ind4], autopct=make_autopct(fracsq4[ind4]),
                shadow=True)  # , startangle=90)

        ax.text(0.02, 1.05, wsn[ws], fontsize=20)
        ax.text(0.117647 + 0.031594, .97, "I felt comfortable asking \nquestions at this workshop",
                verticalalignment='top', fontsize=12)
        ax.text(0.618342 + 0.031394, .97, "I enjoyed the workshop and \nlearned something interesting",
                verticalalignment='top', fontsize=12)
        ax.text(0.117647 + 0.031594, .60, "I think I would enjoy having \nthe workshop leaders' job",
                verticalalignment='top', fontsize=12)
        ax.text(0.618342, .60, "The workshop made me feel that I \ncan have a career in STEM", verticalalignment='top',
                fontsize=12)
        ax.axis('off')

        stuff = ''
        stuff2 = ''
        stuff_count = 0
        text_file = open(wsn[ws] + '.txt', "w")
        for j in range(len(cmts)):
            if len(cmts[j]) > 0:
                text_file.write(cmts[j])
                text_file.write('\n')
                if stuff_count < 100:

                    stuff_count = stuff_count + 1
                    if len(cmts[j]) < 120:
                        stuff = stuff + str(stuff_count) + '. ' + cmts[j] + '\n'
                    else:
                        cc = list(cmts[j])
                        cc[100] = '\n'
                        cmts_rj = "".join(cc)
                        stuff = stuff + str(stuff_count) + '. ' + cmts_rj + '\n'
                        print stuff

                else:
                    stuff2 = stuff2 + cmts[j] + '\n'
        text_file.close()

        if stuff_count < 18:
            ax.text(0.02, 0.02, stuff, fontsize=10)
        else:
            ax.text(0.02, 0.02, stuff, fontsize=9)

        plt.savefig(wsn[ws] + '.pdf')

        plt.close()
