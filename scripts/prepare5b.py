#!/usr/bin/env python
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pymongo import MongoClient
import scipy.stats as stats

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
"
sentiment = []

for i in cursor:
	
	if i["sentiment"]["type"] == u'neutral':
		sentiment.append(0)
	else:
		ia = float(i["sentiment"]["score"])
		ia = round(ia, 2)
		sentiment.append(ia)

# print sentiment

"""

sentiment =  [0.19, -0.06, -0.24, 0.15, -0.64, -0.66, -0.04, -0.06, 0.24, 0.11, -0.2, -0.2, 0.03, 0.17, 0.49, -0.1, 0.29, 0.28, 0.24, -0.49, -0.26, -0.17, -0.21, 0.61, 0.18, -0.17, -0.33, -0.28, -0.46, 0.25, 0.13, 0.23, -0.1, -0.02, -0.04, 0.11, -0.13, 0.05, -0.32, -0.48, 0.15, 0.48, 0.11, -0.13, 0.14, 0.27, 0.04, 0.19, 0.12, -0.48, -0.43, 0.44, 0.77, -0.21, -0.05, -0.17, -0.09, 0.37, 0.78, 0.19, -0.38, 0.6, 0.46, -0.04, 0.19, -0.41, 0.46, 0.05, 0.04, -0.24, -0.13, -0.15, 0.53, 0.55, -0.14, -0.21, -0.07, -0.33, -0.72, -0.28, 0.01, -0.01, 0.33, -0.39, 0.11, 0.27, 0.67, -0.1, -0.24, 0.48, -0.57, 0.3, 0.68, -0.16, 0.65, -0.61, 0.59, 0.54, -0.13, -0.1, 0.05, 0.7, 0.69, 0.35, -0.26, 0.48, -0.08, 0.41, 0.4, -0.44, 0.26, 0.22, 0.18, 0.3, -0.29, -0.31, -0.41, -0.17, -0.6, 0.25, -0.2, -0.62, -0.09, 0.47, -0.06, 0.35, 0.81, 0.6, -0.4, 0.34, -0.33, 0.21, 0.51, -0.03, 0.02, -0.04, 0.68, -0.06, 0.03, 0.6, -0.01, 0.42, -0.1, 0.27, -0.04, -0.37, 0.48, 0.21, 0.15, -0.05, 0.39, -0.05, 0.29, -0.6, 0.08, -0.04, 0.23, -0.33, 0.14, -0.0, 0.03, -0.77, 0.17, 0.06, 0.26, -0.61, 0.4, -0.06, -0.24, 0.31, -0.62, 0.22, 0.2, 0.05, 0.19, 0.23, -0.41, -0.14, -0.12, 0.74, 0.52, -0.56, 0.6, 0.7, 0.11, -0.34, -0.42, -0.25, 0.41, -0.18, -0.43, -0.7, -0.16, 0.22, 0.24, 0.62, 0.05, 0.22, -0.0, 0.29, -0.45, 0.39, -0.06, 0.1, -0.07, 0.79, -0.57, 0.99, -0.42, -0.31, -0.68, 0.57, -0.1, -0.24, 0.38, 0.08, -0.13, 0.25, 0.34, -0.46, 0.44, 0.45, 0.12, 0.02, -0.02, -0.54, 0.37, 0.33, 0.01, -0.47, 0.19, 0.1, 0.1, -0.37, -0.21, 0.46, -0.42, -0.68, 0.1, 0.21, 0.13, 0.32, -0.47, -0.62, -0.05, 0.0, 0.07, -0.12, 0.06, 0.46, 0.37, 0.7, -0.78, 0.25, 0.4, 0.72, 0.43, 0.5, -0.16, -0.04, 0.36, 0.25, 0.88, -0.12, 0.49, 0.7, -0.25, -0.46, 0.4, 0.64, 0.57, -0.22, 0.27, 0.58, 0.09, -0.18, -0.15, 0, -0.39, 0.4, 0.15, 0.22, -0.34, 0.24, 0.56, -0.4, 0.18, -0.1, 0.73, 0.08, -0.18, -0.11, 0.33, 0.03, 0.15, -0.3, 0.62, 0.03, 0.09, 0.84, 0.86, 0.86, 0.33, -0.1, 0.53, -0.11, 0.31, 0.22, 0.73, -0.16, 0.34, 0.22, -0.39, -0.44, -0.25, 0.41, 0.45, 0.15, -0.61, -0.35, 0.43, 0.33, 0.25, -0.53, -0.2, 0.43, -0.44, 0.08, 0.52, 0.45, -0.39, 0.2, 0.78, -0.15, -0.09, -0.11, 0.32, 0.36, 0.16, -0.69, 0.16, -0.22, 0.49, 0.09, 0.23, 0.69, 0.11, -0.17, 0.34, 0.85, -0.12, 0.32, -0.21, 0.75, 0.06, -0.16, -0.1, 0.67, 0.1, 0.46, -0.33, -0.34, 0.43, -0.38, 0.58, 0.06, 0.05, -0.22, 0.35, 0.04, 0.08, 0.46, 0.23, 0.64, 0.37, 0.34, -0.89, 0.11, 0.82, -0.25, -0.36, -0.1, -0.29, 0.32, 0.6, -0.11, 0.14, -0.65, 0.11, 0.56, 0.34, -0.19, -0.6, -0.38, 0.39, 0.03, -0.62, 0.62, 0.6, 0.05, -0.09, 0.08, 0.09, -0.02, 0.38, 0.24, -0.64, 0.62, 0.36, -0.2, -0.28, -0.1, -0.41, 0.6, 0.29, 0.36, -0.09, 0.07, 0.05, -0.17, 0.81, 0.44, 0.84, 0.38, 0.39, 0.01, 0.04, 0.52, -0.35, -0.43, 0.27, -0.43, 0.38, 0.05, 0.5, 0.45, 0.12, 0.37, 0.21, -0.34, -0.81, 0.57, -0.28, -0.42, -0.0, -0.77, 0.15, 0.68, -0.1, 0.24, -0.23, 0.44, 0.09, -0.08, -0.21, 0.52, -0.1, 0.62, -0.45, 0.47, 0.19, -0.44, 0.17, -0.2, 0.66, 0.27, -0.35, -0.49, -0.06, 0.07, 0.21, -0.25, 0.68, -0.36, 0.06, 0.06, 0.23, -0.64, -0.34, 0.3, -0.12, -0.39, 0.5, 0.42, -0.33, 0.11, -0.17, -0.36, 0.32, -0.49, -0.63, 0.19, 0.4, 0.06, -0.24, -0.31, 0.25, -0.01, 0.3, 0.66, 0.41, 0.12, 0.16, -0.78, -0.11, -0.04, 0.76, 0.07, 0.64, -0.38, -0.44, -0.16, 0.35, 0.9, 0.64, 0.24, 0.37, 0.42, 0.85, 0.88, -0.47, 0.79, 0.75, 0.64, 0.27, 0.08, -0.54, -0.1, 0.78, 0.5, 0.5, -0.69, 0.4, -0.68, 0.47, 0.34, 0.37, 0.03, 0.35, 0.03, 0.5, 0.46, 0.42, -0.2, 0.1, -0.57, -0.32, 0.72, 0.91, 0.55, -0.18, 0.01, -0.56, 0.3, 0.24, 0.19, 0.2, 0.33, 0.49, -0.57, 0.86, -0.04, 0.39, 0.49, 0.14, -0.22, 0.7, 0.39, 0.1, 0.63, 0.41, -0.38, 0.5, 0.48, 0.01, 0.36, -0.12, 0.15, 0.26, 0.16, 0.31, 0.96, 0.28, 0.69, -0.2, -0.18, -0.05, 0.45, -0.24, -0.5, -0.5, -0.01, 0.13, -0.27, 0.95, 0.47, -0.07, -0.13, -0.27, -0.45, -0.65, -0.31, -0.73, 0.51, -0.08, -0.19, 0.21, 0.06, 0.22, 0.14, 0.23, -0.6, 0.26, 0.46, -0.51, 0.05, 0.02, 0.4, 0.02, -0.42, 0.76, -0.31, -0.11, 0.37, -0.04, -0.28, -0.11, -0.03, 0.42, 0.26, 0.02, 0.42, 0, -0.31, 0.16, -0.3, 0.19, 0.46, 0.72, 0.34, -0.22, 0.41, 0.34, 0.11, 0.17, 0.1, 0.28, 0.03, 0.02, 0.25, -0.29, 0.09, -0.51, -0.8, -0.51, 0.68, -0.2, 0.14, -0.05, -0.61, 0.87, -0.23, 0.17, -0.35, -0.05, 0.29, 0.37, -0.18, 0.39, -0.42, -0.32, 0.54, 0.07, 0.21, -0.73, 0.15, -0.23, 0.09, -0.41, 0.52, 0.51, -0.22, -0.39, -0.29, 0.29, 0.14, -0.08, -0.16, 0.17, -0.42, -0.2, 0.38, -0.23, 0.13, 0.84, 0.18, -0.79, -0.36, 0.52, -0.42, -0.47, -0.07, 0.33, 0.5, 0.47, 0.26, -0.26, -0.48, 0.24, 0.5, -0.54, 0.21, -0.22, 0.04, -0.64, -0.15, -0.12, 0.69, -0.05, -0.25, 0.52, 0.23, -0.66, -0.09, 0.53, 0.59, -0.15, 0.58, 0.38, 0.49, 0.72, 0.47, 0.82, 0.06, 0.28, 0.32, 0.15, -0.93, 0.35, 0.44, -0.29, -0.12, 0.48, 0.34, 0.33, 0.43, 0.49, 0.12, 0.45, 0.39, 0.42, 0.15, -0.11, -0.21, 0.47, 0.46, 0.11, -0.26, 0.29, 0.63, 0.05, -0.5, 0.41, -0.18, 0.49, 0.45, 0.15, -0.2, -0.32, 0.24, -0.29, 0.4, 0.42, 0.49, -0.29, 0.51, 0.39, -0.14, -0.03, 0.04, 0.26, 0.87, 0.39, -0.21, 0.43, -0.19, 0.71, 0.36, 0.02, 0.08, -0.2, 0.3, 0.2, -0.78, -0.05, -0.33, -0.13, 0.51, 0.41, 0.64, 0.16, 0.5, 0.21, 0.12, 0.54, -0.76, -0.76, -0.08, 0.17, 0.33, -0.26, -0.55, 0.7, -0.31, -0.29, -0.35, 0.02, 0.78, 0.06, -0.13, -0.59, 0.42, -0.68, 0.2, -0.1, 0.55, 0.68, -0.57, -0.13, -0.54, -0.05, -0.27, -0.39, 0.62, 0.36, -0.06, 0.23, 0.64, 0.64, 0.2, 0.59, 0.38, 0.75, 0.59, 0.5, 0.56, 0.39, 0.27, -0.31, 0.63, 0.19, 0.32, -0.3, 0.61, -0.02, -0.31, -0.0, 0.07, -0.02, 0.65, -0.15, 0.46, 0.28, 0.4, 0.42, 0.64, 0.45, 0.16, -0.15, 0.29, 0.38, -0.63, -0.12, -0.51, -0.16, -0.09, 0.2, -0.24, -0.35, 0.38, 0.68, 0.71, 0.49, 0.65, 0.47, -0.42, 0.43, 0.06, -0.18, 0.3, 0.55, 0.92, -0.14, 0.64, 0.14, 0.15, 0.76, 0.23, 0.48, 0.14, 0.7, 0.11, -0.0, 0.63, -0.29, 0.85, 0.17, 0.32, 0.6, -0.13, 0.4, 0.72, -0.44, 0.22, -0.31, -0.49, 0.71, 0.14, 0.14, 0.73, 0.24, 0.21, -0.21, -0.44, 0.35, 0.58, 0.66, -0.2, -0.45, 0.7, 0.24, 0.11, -0.36, 0.34, 0.22, -0.63, 0.59, 0.36, -0.56, 0.01, -0.28, -0.46, 0.05, 0.35, -0.23, -0.88, 0.47, 0.26, 0.8, -0.34, 0.19, 0.57, 0.82, 0.12, 0.68, -0.06, 0.81, 0.39, -0.21, 0.34, 0.32, 0.25, 0.24, -0.51, -0.42, 0.03, -0.92, -0.42, -0.13, -0.12, 0.28, 0.05, 0.69, -0.34, -0.24, 0.3, 0.19, 0.09, 0.04, -0.47, 0.05, -0.4, -0.59, -0.4, 0.25, 0.02, 0.16]


senMean = np.mean(sentiment)
senStd = np.std(sentiment)

sentiment[:] = [round(x - senMean, 2) for x in sentiment]
sentiment[:] = [round(x / senStd, 2) for x in sentiment]


print np.mean(sentiment)

# attr = stats.normaltest(sentiment[0:20])
# plots the p value
# print attr[1]

notNormal = []
iter = range(0, len(sentiment) - 21, 1)


for it in iter:
	a1 = stats.normaltest(sentiment[it:(it+20)])
	if a1[1] < 0.05:
		itavg = np.mean(sentiment[it:(it+20)])
		itadd = [it, itavg]
		notNormal.append(itadd)
		
print notNormal

# client.close()
# print "Disconnected."

# plt.plot(sentiment, 'g')
# plt.axhline(y = (senMean - 2 * senStd), linewidth=1, color = 'r')
# plt.axhline(y = (senMean), linewidth=1, color = 'm') # , xmin=0.25, xmax=0.402

# plt.show()

# print sentiment

