import analytic
import thinkstats2
import thinkplot

df = analytic.ReadBabyBoom()
diffs = df.minutes.diff()

cdf = thinkstats2.Cdf(diffs, label='actual')
# thinkplot.Cdf(cdf)
# thinkplot.Show(xlabel='minutes', ylabel='CDF')

import scipy.stats

mean = 178
sd = 7.7
min = 177.8
max = 185.4
min_prob = scipy.stats.norm.cdf(min, loc=mean, scale=sd)
max_prob = scipy.stats.norm.cdf(max, loc=mean, scale=sd)

