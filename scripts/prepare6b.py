#!/usr/bin/env python
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pymongo import MongoClient
import scipy.stats as stats


"""
Access data from database and make a basic histogram plot.

"""




client = MongoClient('localhost', 27017)
if client is None:
    print "Couldn't connect!"
else:
    print ("Connected.")



# change dbc values to the ones appropriate for your setup.

dbc = client.mongo2.review_2  # ...


# Query database - get data in ascendiong date.
# print results with limit on to see them
cursor = dbc.find({"business_id": "zTCCbg7mGslxACL5KlAPIQ"}).sort("date", 1)#.limit(20)

# print cursor.count()
# 987 reviews.



"""

Data Schema:

[[Month #, "month_string", sent1,sent2, ...], 
... ]

"""

"""
# Pre initialize data


month = 0
mnstr = "0123456"
		
revStatsData = []
sentiment = []

for i in cursor:
	# print str([i["date"][0:7], i["sentiment"]["score"]])
	if i["date"][0:7] == mnstr:
		if i["sentiment"]["type"] == u'neutral':
			sentiment.append(0)
		else:
			ia = float(i["sentiment"]["score"])
			ia = round(ia, 2)
			sentiment.append(ia)		
			
	else:
		# Debugging: 
		# print "New Month!"
		# print i["date"][0:7]
		# print mnstr
		
		if month != 0:
			revStatsData.append([month, mnstr, sentiment])
		
		mnstr = i["date"][0:7]
		month += 1
		sentiment =[]
		
		if i["sentiment"]["type"] == u'neutral':
			sentiment.append(0)
		else:
			ia = float(i["sentiment"]["score"])
			ia = round(ia, 2)
			sentiment.append(ia)
revStatsData.append([month, mnstr, sentiment])
			
print revStatsData

"""

revStatsData = [[1, u'2009-12', [0.19, -0.06, -0.24, 0.15, -0.64, -0.66, -0.04, -0.06, 0.24, 0.11, -0.2, -0.2, 0.03, 0.17, 0.49, -0.1, 0.29, 0.28]], [2, u'2010-01', [0.24, -0.49, -0.26, -0.17, -0.21, 0.61, 0.18, -0.17, -0.33, -0.28, -0.46, 0.25, 0.13, 0.23, -0.1, -0.02, -0.04, 0.11, -0.13, 0.05, -0.32, -0.48, 0.15, 0.48, 0.11]], [3, u'2010-02', [-0.13, 0.14, 0.27, 0.04, 0.19, 0.12, -0.48, -0.43, 0.44, 0.77, -0.21, -0.05, -0.17, -0.09]], [4, u'2010-03', [0.37, 0.78, 0.19, -0.38, 0.6, 0.46, -0.04, 0.19, -0.41, 0.46, 0.05, 0.04, -0.24, -0.13, -0.15, 0.53]], [5, u'2010-04', [0.55, -0.14, -0.21, -0.07, -0.33, -0.72, -0.28, 0.01, -0.01, 0.33, -0.39, 0.11, 0.27, 0.67, -0.1, -0.24]], [6, u'2010-05', [0.48, -0.57, 0.3, 0.68, -0.16, 0.65, -0.61, 0.59, 0.54, -0.13, -0.1, 0.05, 0.7, 0.69, 0.35, -0.26, 0.48, -0.08, 0.41, 0.4, -0.44, 0.26, 0.22]], [7, u'2010-06', [0.18, 0.3, -0.29, -0.31, -0.41, -0.17, -0.6, 0.25, -0.2, -0.62, -0.09, 0.47, -0.06, 0.35, 0.81, 0.6, -0.4]], [8, u'2010-07', [0.34, -0.33, 0.21, 0.51, -0.03, 0.02, -0.04, 0.68, -0.06, 0.03, 0.6, -0.01, 0.42, -0.1, 0.27, -0.04, -0.37, 0.48, 0.21, 0.15]], [9, u'2010-08', [-0.05, 0.39, -0.05, 0.29, -0.6, 0.08, -0.04, 0.23, -0.33, 0.14, -0.0, 0.03, -0.77, 0.17, 0.06, 0.26, -0.61, 0.4, -0.06, -0.24, 0.31, -0.62, 0.22]], [10, u'2010-09', [0.2, 0.05, 0.19, 0.23, -0.41, -0.14, -0.12, 0.74, 0.52, -0.56, 0.6, 0.7, 0.11, -0.34]], [11, u'2010-10', [-0.42, -0.25, 0.41, -0.18, -0.43, -0.7, -0.16, 0.22, 0.24, 0.62, 0.05, 0.22, -0.0, 0.29]], [12, u'2010-11', [-0.45, 0.39, -0.06, 0.1, -0.07, 0.79, -0.57, 0.99, -0.42, -0.31, -0.68, 0.57, -0.1, -0.24, 0.38, 0.08]], [13, u'2010-12', [-0.13, 0.25, 0.34, -0.46, 0.44, 0.45, 0.12, 0.02, -0.02, -0.54, 0.37, 0.33, 0.01, -0.47, 0.19, 0.1]], [14, u'2011-01', [0.1, -0.37, -0.21, 0.46, -0.42, -0.68, 0.1, 0.21, 0.13, 0.32, -0.47, -0.62, -0.05, 0.0]], [15, u'2011-02', [0.07, -0.12, 0.06, 0.46, 0.37, 0.7, -0.78, 0.25, 0.4, 0.72, 0.43, 0.5, -0.16]], [16, u'2011-03', [-0.04, 0.36, 0.25, 0.88, -0.12, 0.49, 0.7, -0.25, -0.46, 0.4, 0.64, 0.57, -0.22, 0.27, 0.58, 0.09, -0.18, -0.15, 0, -0.39, 0.4, 0.15, 0.22, -0.34]], [17, u'2011-04', [0.24, 0.56, -0.4, 0.18, -0.1, 0.73, 0.08, -0.18, -0.11, 0.33, 0.03]], [18, u'2011-05', [0.15, -0.3, 0.62, 0.03, 0.09, 0.84, 0.86, 0.86, 0.33, -0.1, 0.53]], [19, u'2011-06', [-0.11, 0.31, 0.22, 0.73, -0.16, 0.34, 0.22, -0.39, -0.44, -0.25, 0.41, 0.45, 0.15, -0.61, -0.35, 0.43, 0.33, 0.25]], [20, u'2011-07', [-0.53, -0.2, 0.43, -0.44, 0.08, 0.52, 0.45, -0.39, 0.2, 0.78, -0.15, -0.09, -0.11, 0.32, 0.36, 0.16, -0.69, 0.16]], [21, u'2011-08', [-0.22, 0.49, 0.09, 0.23, 0.69, 0.11, -0.17, 0.34, 0.85, -0.12, 0.32]], [22, u'2011-09', [-0.21, 0.75, 0.06, -0.16, -0.1, 0.67, 0.1, 0.46, -0.33, -0.34, 0.43]], [23, u'2011-10', [-0.38, 0.58, 0.06, 0.05, -0.22, 0.35]], [24, u'2011-11', [0.04, 0.08, 0.46, 0.23, 0.64, 0.37, 0.34, -0.89, 0.11, 0.82]], [25, u'2011-12', [-0.25, -0.36, -0.1, -0.29, 0.32, 0.6, -0.11, 0.14, -0.65, 0.11]], [26, u'2012-01', [0.56, 0.34, -0.19, -0.6, -0.38, 0.39, 0.03, -0.62, 0.62, 0.6, 0.05, -0.09, 0.08, 0.09, -0.02, 0.38, 0.24, -0.64, 0.62, 0.36, -0.2]], [27, u'2012-02', [-0.28, -0.1, -0.41, 0.6, 0.29, 0.36, -0.09, 0.07, 0.05, -0.17, 0.81]], [28, u'2012-03', [0.44, 0.84, 0.38, 0.39, 0.01, 0.04, 0.52, -0.35, -0.43, 0.27, -0.43, 0.38, 0.05, 0.5]], [29, u'2012-04', [0.45, 0.12, 0.37, 0.21, -0.34, -0.81, 0.57, -0.28, -0.42, -0.0, -0.77]], [30, u'2012-05', [0.15, 0.68, -0.1, 0.24, -0.23, 0.44, 0.09, -0.08, -0.21, 0.52, -0.1, 0.62, -0.45, 0.47]], [31, u'2012-06', [0.19, -0.44, 0.17, -0.2, 0.66, 0.27, -0.35, -0.49, -0.06, 0.07, 0.21, -0.25, 0.68]], [32, u'2012-07', [-0.36, 0.06, 0.06, 0.23, -0.64, -0.34, 0.3, -0.12, -0.39, 0.5, 0.42, -0.33, 0.11, -0.17, -0.36, 0.32, -0.49, -0.63, 0.19, 0.4, 0.06, -0.24]], [33, u'2012-08', [-0.31, 0.25, -0.01, 0.3, 0.66, 0.41, 0.12, 0.16, -0.78, -0.11, -0.04, 0.76, 0.07, 0.64, -0.38]], [34, u'2012-09', [-0.44, -0.16, 0.35, 0.9, 0.64, 0.24, 0.37, 0.42, 0.85, 0.88]], [35, u'2012-10', [-0.47, 0.79, 0.75, 0.64, 0.27, 0.08, -0.54, -0.1, 0.78, 0.5, 0.5, -0.69]], [36, u'2012-11', [0.4, -0.68, 0.47, 0.34]], [37, u'2012-12', [0.37, 0.03, 0.35, 0.03, 0.5, 0.46, 0.42, -0.2, 0.1]], [38, u'2013-01', [-0.57, -0.32, 0.72, 0.91, 0.55, -0.18, 0.01, -0.56, 0.3, 0.24, 0.19, 0.2, 0.33, 0.49, -0.57, 0.86, -0.04, 0.39]], [39, u'2013-02', [0.49, 0.14, -0.22, 0.7, 0.39, 0.1, 0.63, 0.41, -0.38, 0.5, 0.48, 0.01, 0.36, -0.12, 0.15, 0.26, 0.16, 0.31]], [40, u'2013-03', [0.96, 0.28, 0.69, -0.2, -0.18, -0.05, 0.45, -0.24, -0.5, -0.5, -0.01]], [41, u'2013-04', [0.13, -0.27, 0.95, 0.47, -0.07, -0.13, -0.27, -0.45, -0.65, -0.31, -0.73, 0.51, -0.08, -0.19, 0.21, 0.06]], [42, u'2013-05', [0.22, 0.14, 0.23, -0.6, 0.26, 0.46, -0.51, 0.05, 0.02, 0.4, 0.02, -0.42, 0.76, -0.31, -0.11]], [43, u'2013-06', [0.37, -0.04, -0.28, -0.11, -0.03, 0.42, 0.26, 0.02, 0.42, 0, -0.31, 0.16, -0.3, 0.19, 0.46, 0.72, 0.34, -0.22, 0.41, 0.34, 0.11, 0.17]], [44, u'2013-07', [0.1, 0.28, 0.03, 0.02, 0.25, -0.29, 0.09, -0.51, -0.8, -0.51, 0.68, -0.2, 0.14, -0.05, -0.61, 0.87, -0.23, 0.17]], [45, u'2013-08', [-0.35, -0.05, 0.29, 0.37, -0.18, 0.39, -0.42, -0.32, 0.54, 0.07, 0.21, -0.73, 0.15, -0.23, 0.09, -0.41, 0.52, 0.51, -0.22, -0.39, -0.29, 0.29, 0.14, -0.08, -0.16]], [46, u'2013-09', [0.17, -0.42, -0.2, 0.38, -0.23, 0.13, 0.84, 0.18, -0.79, -0.36, 0.52, -0.42, -0.47]], [47, u'2013-10', [-0.07, 0.33, 0.5, 0.47, 0.26, -0.26, -0.48, 0.24, 0.5, -0.54, 0.21, -0.22, 0.04, -0.64, -0.15, -0.12, 0.69, -0.05, -0.25, 0.52, 0.23, -0.66, -0.09, 0.53]], [48, u'2013-11', [0.59, -0.15, 0.58, 0.38, 0.49, 0.72, 0.47, 0.82, 0.06, 0.28, 0.32, 0.15, -0.93, 0.35, 0.44]], [49, u'2013-12', [-0.29, -0.12, 0.48, 0.34, 0.33, 0.43, 0.49, 0.12, 0.45, 0.39, 0.42, 0.15, -0.11, -0.21, 0.47, 0.46, 0.11]], [50, u'2014-01', [-0.26, 0.29, 0.63, 0.05, -0.5, 0.41, -0.18, 0.49, 0.45, 0.15, -0.2]], [51, u'2014-02', [-0.32, 0.24, -0.29, 0.4, 0.42, 0.49, -0.29, 0.51, 0.39, -0.14, -0.03, 0.04, 0.26, 0.87, 0.39, -0.21, 0.43, -0.19, 0.71, 0.36, 0.02, 0.08]], [52, u'2014-03', [-0.2, 0.3, 0.2, -0.78, -0.05, -0.33, -0.13, 0.51, 0.41, 0.64, 0.16, 0.5, 0.21, 0.12, 0.54, -0.76, -0.76, -0.08, 0.17, 0.33]], [53, u'2014-04', [-0.26, -0.55, 0.7, -0.31, -0.29, -0.35, 0.02, 0.78, 0.06, -0.13, -0.59, 0.42, -0.68, 0.2, -0.1, 0.55, 0.68]], [54, u'2014-05', [-0.57, -0.13, -0.54, -0.05, -0.27, -0.39, 0.62, 0.36, -0.06, 0.23, 0.64, 0.64]], [55, u'2014-06', [0.2, 0.59, 0.38, 0.75, 0.59, 0.5, 0.56, 0.39, 0.27, -0.31, 0.63, 0.19, 0.32, -0.3, 0.61, -0.02]], [56, u'2014-07', [-0.31, -0.0, 0.07, -0.02, 0.65, -0.15, 0.46, 0.28, 0.4, 0.42, 0.64, 0.45, 0.16, -0.15, 0.29, 0.38, -0.63, -0.12, -0.51, -0.16, -0.09, 0.2, -0.24, -0.35, 0.38, 0.68, 0.71, 0.49]], [57, u'2014-08', [0.65, 0.47, -0.42, 0.43, 0.06, -0.18, 0.3, 0.55, 0.92, -0.14, 0.64, 0.14, 0.15, 0.76, 0.23, 0.48, 0.14, 0.7, 0.11, -0.0, 0.63, -0.29, 0.85, 0.17, 0.32, 0.6, -0.13, 0.4]], [58, u'2014-09', [0.72, -0.44, 0.22, -0.31, -0.49, 0.71, 0.14, 0.14, 0.73, 0.24, 0.21, -0.21, -0.44, 0.35, 0.58, 0.66]], [59, u'2014-10', [-0.2, -0.45, 0.7, 0.24, 0.11, -0.36, 0.34, 0.22, -0.63, 0.59, 0.36, -0.56, 0.01, -0.28, -0.46, 0.05, 0.35, -0.23, -0.88, 0.47, 0.26]], [60, u'2014-11', [0.8, -0.34, 0.19, 0.57, 0.82, 0.12, 0.68, -0.06, 0.81, 0.39, -0.21, 0.34, 0.32, 0.25, 0.24, -0.51, -0.42, 0.03, -0.92, -0.42, -0.13, -0.12]], [61, u'2014-12', [0.28, 0.05, 0.69, -0.34, -0.24, 0.3, 0.19, 0.09, 0.04, -0.47, 0.05]], [62, u'2015-01', [-0.4, -0.59, -0.4, 0.25, 0.02, 0.16]]]
iter = range(1,61,2)


data1 = []

for it in iter:
	
	ita = revStatsData[it][2]
	for iit in revStatsData[it+1][2]:
		ita.append(iit)
	
	data1.append(ita)

print data1
print len(data1)

	
	
month2Avg = []
for it in data1:
	month2Avg.append(round(np.mean(it),2))
# sample plot - needs improvement

plt.plot(month2Avg, 'g')

plt.show()



"""
[[0.24, -0.49, -0.26, -0.17, -0.21, 0.61, 0.18, -0.17, -0.33, -0.28, -0.46, 0.25, 0.13, 0.23, -0.1, -0.02, -0.04, 0.11, -0.13, 0.05, -0.32, -0.48, 0.15, 0.48, 0.11, -0.13, 0.14, 0.27, 0.04, 0.19, 0.12, -0.48, -0.43, 0.44, 0.77, -0.21, -0.05, -0.17, -0.09], [0.37, 0.78, 0.19, -0.38, 0.6, 0.46, -0.04, 0.19, -0.41, 0.46, 0.05, 0.04, -0.24, -0.13, -0.15, 0.53, 0.55, -0.14, -0.21, -0.07, -0.33, -0.72, -0.28, 0.01, -0.01, 0.33, -0.39, 0.11, 0.27, 0.67, -0.1, -0.24], [0.48, -0.57, 0.3, 0.68, -0.16, 0.65, -0.61, 0.59, 0.54, -0.13, -0.1, 0.05, 0.7, 0.69, 0.35, -0.26, 0.48, -0.08, 0.41, 0.4, -0.44, 0.26, 0.22, 0.18, 0.3, -0.29, -0.31, -0.41, -0.17, -0.6, 0.25, -0.2, -0.62, -0.09, 0.47, -0.06, 0.35, 0.81, 0.6, -0.4], [0.34, -0.33, 0.21, 0.51, -0.03, 0.02, -0.04, 0.68, -0.06, 0.03, 0.6, -0.01, 0.42, -0.1, 0.27, -0.04, -0.37, 0.48, 0.21, 0.15, -0.05, 0.39, -0.05, 0.29, -0.6, 0.08, -0.04, 0.23, -0.33, 0.14, -0.0, 0.03, -0.77, 0.17, 0.06, 0.26, -0.61, 0.4, -0.06, -0.24, 0.31, -0.62, 0.22], [0.2, 0.05, 0.19, 0.23, -0.41, -0.14, -0.12, 0.74, 0.52, -0.56, 0.6, 0.7, 0.11, -0.34, -0.42, -0.25, 0.41, -0.18, -0.43, -0.7, -0.16, 0.22, 0.24, 0.62, 0.05, 0.22, -0.0, 0.29], [-0.45, 0.39, -0.06, 0.1, -0.07, 0.79, -0.57, 0.99, -0.42, -0.31, -0.68, 0.57, -0.1, -0.24, 0.38, 0.08, -0.13, 0.25, 0.34, -0.46, 0.44, 0.45, 0.12, 0.02, -0.02, -0.54, 0.37, 0.33, 0.01, -0.47, 0.19, 0.1], [0.1, -0.37, -0.21, 0.46, -0.42, -0.68, 0.1, 0.21, 0.13, 0.32, -0.47, -0.62, -0.05, 0.0, 0.07, -0.12, 0.06, 0.46, 0.37, 0.7, -0.78, 0.25, 0.4, 0.72, 0.43, 0.5, -0.16], [-0.04, 0.36, 0.25, 0.88, -0.12, 0.49, 0.7, -0.25, -0.46, 0.4, 0.64, 0.57, -0.22, 0.27, 0.58, 0.09, -0.18, -0.15, 0, -0.39, 0.4, 0.15, 0.22, -0.34, 0.24, 0.56, -0.4, 0.18, -0.1, 0.73, 0.08, -0.18, -0.11, 0.33, 0.03], [0.15, -0.3, 0.62, 0.03, 0.09, 0.84, 0.86, 0.86, 0.33, -0.1, 0.53, -0.11, 0.31, 0.22, 0.73, -0.16, 0.34, 0.22, -0.39, -0.44, -0.25, 0.41, 0.45, 0.15, -0.61, -0.35, 0.43, 0.33, 0.25], [-0.53, -0.2, 0.43, -0.44, 0.08, 0.52, 0.45, -0.39, 0.2, 0.78, -0.15, -0.09, -0.11, 0.32, 0.36, 0.16, -0.69, 0.16, -0.22, 0.49, 0.09, 0.23, 0.69, 0.11, -0.17, 0.34, 0.85, -0.12, 0.32], [-0.21, 0.75, 0.06, -0.16, -0.1, 0.67, 0.1, 0.46, -0.33, -0.34, 0.43, -0.38, 0.58, 0.06, 0.05, -0.22, 0.35], [0.04, 0.08, 0.46, 0.23, 0.64, 0.37, 0.34, -0.89, 0.11, 0.82, -0.25, -0.36, -0.1, -0.29, 0.32, 0.6, -0.11, 0.14, -0.65, 0.11], [0.56, 0.34, -0.19, -0.6, -0.38, 0.39, 0.03, -0.62, 0.62, 0.6, 0.05, -0.09, 0.08, 0.09, -0.02, 0.38, 0.24, -0.64, 0.62, 0.36, -0.2, -0.28, -0.1, -0.41, 0.6, 0.29, 0.36, -0.09, 0.07, 0.05, -0.17, 0.81], [0.44, 0.84, 0.38, 0.39, 0.01, 0.04, 0.52, -0.35, -0.43, 0.27, -0.43, 0.38, 0.05, 0.5, 0.45, 0.12, 0.37, 0.21, -0.34, -0.81, 0.57, -0.28, -0.42, -0.0, -0.77], [0.15, 0.68, -0.1, 0.24, -0.23, 0.44, 0.09, -0.08, -0.21, 0.52, -0.1, 0.62, -0.45, 0.47, 0.19, -0.44, 0.17, -0.2, 0.66, 0.27, -0.35, -0.49, -0.06, 0.07, 0.21, -0.25, 0.68], [-0.36, 0.06, 0.06, 0.23, -0.64, -0.34, 0.3, -0.12, -0.39, 0.5, 0.42, -0.33, 0.11, -0.17, -0.36, 0.32, -0.49, -0.63, 0.19, 0.4, 0.06, -0.24, -0.31, 0.25, -0.01, 0.3, 0.66, 0.41, 0.12, 0.16, -0.78, -0.11, -0.04, 0.76, 0.07, 0.64, -0.38], [-0.44, -0.16, 0.35, 0.9, 0.64, 0.24, 0.37, 0.42, 0.85, 0.88, -0.47, 0.79, 0.75, 0.64, 0.27, 0.08, -0.54, -0.1, 0.78, 0.5, 0.5, -0.69], [0.4, -0.68, 0.47, 0.34, 0.37, 0.03, 0.35, 0.03, 0.5, 0.46, 0.42, -0.2, 0.1], [-0.57, -0.32, 0.72, 0.91, 0.55, -0.18, 0.01, -0.56, 0.3, 0.24, 0.19, 0.2, 0.33, 0.49, -0.57, 0.86, -0.04, 0.39, 0.49, 0.14, -0.22, 0.7, 0.39, 0.1, 0.63, 0.41, -0.38, 0.5, 0.48, 0.01, 0.36, -0.12, 0.15, 0.26, 0.16, 0.31], [0.96, 0.28, 0.69, -0.2, -0.18, -0.05, 0.45, -0.24, -0.5, -0.5, -0.01, 0.13, -0.27, 0.95, 0.47, -0.07, -0.13, -0.27, -0.45, -0.65, -0.31, -0.73, 0.51, -0.08, -0.19, 0.21, 0.06], [0.22, 0.14, 0.23, -0.6, 0.26, 0.46, -0.51, 0.05, 0.02, 0.4, 0.02, -0.42, 0.76, -0.31, -0.11, 0.37, -0.04, -0.28, -0.11, -0.03, 0.42, 0.26, 0.02, 0.42, 0, -0.31, 0.16, -0.3, 0.19, 0.46, 0.72, 0.34, -0.22, 0.41, 0.34, 0.11, 0.17], [0.1, 0.28, 0.03, 0.02, 0.25, -0.29, 0.09, -0.51, -0.8, -0.51, 0.68, -0.2, 0.14, -0.05, -0.61, 0.87, -0.23, 0.17, -0.35, -0.05, 0.29, 0.37, -0.18, 0.39, -0.42, -0.32, 0.54, 0.07, 0.21, -0.73, 0.15, -0.23, 0.09, -0.41, 0.52, 0.51, -0.22, -0.39, -0.29, 0.29, 0.14, -0.08, -0.16], [0.17, -0.42, -0.2, 0.38, -0.23, 0.13, 0.84, 0.18, -0.79, -0.36, 0.52, -0.42, -0.47, -0.07, 0.33, 0.5, 0.47, 0.26, -0.26, -0.48, 0.24, 0.5, -0.54, 0.21, -0.22, 0.04, -0.64, -0.15, -0.12, 0.69, -0.05, -0.25, 0.52, 0.23, -0.66, -0.09, 0.53], [0.59, -0.15, 0.58, 0.38, 0.49, 0.72, 0.47, 0.82, 0.06, 0.28, 0.32, 0.15, -0.93, 0.35, 0.44, -0.29, -0.12, 0.48, 0.34, 0.33, 0.43, 0.49, 0.12, 0.45, 0.39, 0.42, 0.15, -0.11, -0.21, 0.47, 0.46, 0.11], [-0.26, 0.29, 0.63, 0.05, -0.5, 0.41, -0.18, 0.49, 0.45, 0.15, -0.2, -0.32, 0.24, -0.29, 0.4, 0.42, 0.49, -0.29, 0.51, 0.39, -0.14, -0.03, 0.04, 0.26, 0.87, 0.39, -0.21, 0.43, -0.19, 0.71, 0.36, 0.02, 0.08], [-0.2, 0.3, 0.2, -0.78, -0.05, -0.33, -0.13, 0.51, 0.41, 0.64, 0.16, 0.5, 0.21, 0.12, 0.54, -0.76, -0.76, -0.08, 0.17, 0.33, -0.26, -0.55, 0.7, -0.31, -0.29, -0.35, 0.02, 0.78, 0.06, -0.13, -0.59, 0.42, -0.68, 0.2, -0.1, 0.55, 0.68], [-0.57, -0.13, -0.54, -0.05, -0.27, -0.39, 0.62, 0.36, -0.06, 0.23, 0.64, 0.64, 0.2, 0.59, 0.38, 0.75, 0.59, 0.5, 0.56, 0.39, 0.27, -0.31, 0.63, 0.19, 0.32, -0.3, 0.61, -0.02], [-0.31, -0.0, 0.07, -0.02, 0.65, -0.15, 0.46, 0.28, 0.4, 0.42, 0.64, 0.45, 0.16, -0.15, 0.29, 0.38, -0.63, -0.12, -0.51, -0.16, -0.09, 0.2, -0.24, -0.35, 0.38, 0.68, 0.71, 0.49, 0.65, 0.47, -0.42, 0.43, 0.06, -0.18, 0.3, 0.55, 0.92, -0.14, 0.64, 0.14, 0.15, 0.76, 0.23, 0.48, 0.14, 0.7, 0.11, -0.0, 0.63, -0.29, 0.85, 0.17, 0.32, 0.6, -0.13, 0.4], [0.72, -0.44, 0.22, -0.31, -0.49, 0.71, 0.14, 0.14, 0.73, 0.24, 0.21, -0.21, -0.44, 0.35, 0.58, 0.66, -0.2, -0.45, 0.7, 0.24, 0.11, -0.36, 0.34, 0.22, -0.63, 0.59, 0.36, -0.56, 0.01, -0.28, -0.46, 0.05, 0.35, -0.23, -0.88, 0.47, 0.26], [0.8, -0.34, 0.19, 0.57, 0.82, 0.12, 0.68, -0.06, 0.81, 0.39, -0.21, 0.34, 0.32, 0.25, 0.24, -0.51, -0.42, 0.03, -0.92, -0.42, -0.13, -0.12, 0.28, 0.05, 0.69, -0.34, -0.24, 0.3, 0.19, 0.09, 0.04, -0.47, 0.05]]

"""

client.close()
print "Disconnected."
