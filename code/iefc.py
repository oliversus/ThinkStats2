import numpy as np
import pandas as pd
from __future__ import print_function, division
import scipy.stats

age = 10

pd.set_option('display.mpl_style', 'default')

IEFC_main = '/home/osus/Programming/ThinkStats2/code/IEFC/'
# read csv data
df = pd.read_csv(IEFC_main + 'IEFC_SPA.csv', delimiter=';')
# filter rows of all columns
df_LAI_gt_1 = df[df['LAI_SP'] > 1.] # ... with one condition
df_LAI_gt_1_DBH_lt_DBH_mean = df[(df['LAI_SP'] > 1.) & (df['DBH_SP'] < df['DBH_SP'].mean())] # ... with two conditions
df_LAI_gt_1_SAP_WDD = df[df['LAI_SP'] > 1.][['SAPWOODAREA_SP', 'WOODDENSITY']] # ... only for a few columns
# print summary statistics of dataframe
df_LAI_gt_1_SAP_WDD.describe()
# Column type of a pandas df is pd.Series, which internally is a np array. Adding .values provides np array
dbh_all_np = df.DBH_SP.values
# or to create a Pandas df of one column
dbh_all = df.DBH_SP # df[['DBH_SP']]
# the row index values of a df
dbh_all.index

# filter columns of all rows
df_sub = df[['LAI_SP','SAPWOODAREA_SP','SPECIES','WOODDENSITY','MAX_AGE','FOLIAR_N','GROWTH_SP']]
# return counts of a certain column
df_sub['SPECIES'].value_counts()[:5]
# plot column counts as a bar plot
df_sub['SPECIES'].value_counts()[:10].plot(kind='bar')
# filter rows by species selection
df_sub_3species = df_sub.loc[df_sub['SPECIES'].isin(['Pinus nigra', 'Quercus ilex', 'Pinus sylvestris'])]
psyl = df_sub_3species.loc[df_sub_3species['SPECIES'].isin(['Pinus sylvestris'])]
# return value counts
df_sub_3species['SPECIES'].value_counts()
# plot scatter matrix of a data frame
pd.tools.plotting.scatter_matrix(df_sub_3species, alpha=0.2, diagonal='kde')
pd.tools.plotting.scatter_matrix(psyl, alpha=0.2, diagonal='kde')
# plot (normalized) multi-variate data based on spring tension minimization algorithm
pd.tools.plotting.radviz(df_sub_3species,'SPECIES')

#############################################################################################################

# thinkstats

# print value count sorted by index
df.SPECIES.value_counts().sort_index()

# use Counter to count frequencies
from collections import Counter
t = df.MAX_AGE
counter = Counter(t)
# or Hist from thinkstats2
import thinkstats2 as ts2
hist = ts2.Hist(t, label='max_age')
# print frequency of a value
hist.Freq(20)
# print histogram values
hist.Values()
# iterate values and frequencies
for val, freq in hist.Items():
    print(val, freq)

# plot histogram
import thinkplot as tplt
tplt.Hist(hist)
tplt.Config(xlabel='age', ylabel='frequency')

# for a continuous variable
sapwood = np.floor(df.SAPWOODAREA_SP)
hist = ts2.Hist(sapwood, label='sapwoodarea')
tplt.Hist(hist)
tplt.Config(xlabel='area', ylabel='frequency')

# print smallest/largest values
for area, freq in hist.Smallest(10):
    print(area, freq)
for area, freq in hist.Largest(10):
    print(area, freq)

# print two histograms in one
pnig = df[df.SPECIES == 'Pinus nigra']
not_pnig = df[df.SPECIES != 'Pinus nigra']
qile = df[df.SPECIES == 'Quercus ilex']
pnig_hist = ts2.Hist(pnig.MAX_AGE, label='Pinus nigra')
qile_hist = ts2.Hist(qile.MAX_AGE, label='Quercus ilex')
width = 0.45
tplt.PrePlot(2)
tplt.Hist(pnig_hist, align='right', width=width)
tplt.Hist(qile_hist, align='left', width=width)
tplt.Config(xlabel="age", ylabel="Count")

# summary statistics
pnig.WOODDENSITY.mean()
var = pnig.LAI_SP.var()
std = pnig.LAI_SP.std()
assert(std == var**0.5), "not equal"
pnig.LAI_SP.mean(), not_pnig.LAI_SP.mean()
pnig.LAI_SP.mean() - not_pnig.LAI_SP.mean()

# Cohen effect size: difference in means expressed in # of std
def CohenEffectSize(group1, group2):
    """Computes Cohen's effect size for two groups.

    group1: Series or DataFrame
    group2: Series or DataFrame

    returns: float if the arguments are Series;
             Series if the arguments are DataFrames
    """
    diff = group1.mean() - group2.mean()

    var1 = group1.var()
    var2 = group2.var()
    n1, n2 = len(group1), len(group2)

    pooled_var = (n1 * var1 + n2 * var2) / (n1 + n2)
    d = diff / np.sqrt(pooled_var)
    return d

cohen_pnig_LAI_others = CohenEffectSize(pnig.LAI_SP, not_pnig.LAI_SP)
cohen_pnig_HEIGHT_others = CohenEffectSize(pnig.MAX_HEIGHT, not_pnig.MAX_HEIGHT)
# how do Cohen values compare for LAI vs HEIGHT?
round(abs(cohen_pnig_LAI_others) * 100. / abs(cohen_pnig_HEIGHT_others), 2)

# cumulative distribution functions
cdf_pnig = ts2.Cdf(pnig.MAX_HEIGHT)
tplt.Cdf(cdf_pnig, label='max_height')
cdf_not_pnig = ts2.Cdf(not_pnig.MAX_HEIGHT)
tplt.Cdf(cdf_not_pnig, label='max_height', c='r')
# plot complementary Cdf
# tplt.Cdf(cdf_not_pnig, complement=True)
xs, ps = ts2.RenderNormalCdf(pnig.MAX_HEIGHT.mean(), pnig.MAX_HEIGHT.std(), low=4, high=25)
tplt.Plot(xs, ps, label='model', color='0.8')
# tplt.Plot(xs, xs, color='0.5', style='-')
tplt.Scatter(ps, cdf_pnig.Probs(xs))

# get probability for Nigra being older than 10, and for other trees
age = 10
cdf_pnig.Prob(age)
cdf_not_pnig.Prob(age)
# percentile rank, i.e. Prob * 100
cdf_pnig.PercentileRank(age)
# get median age
cdf_pnig.Value(0.5)
# get inter-quartile range
def inter_quart(cdf):
    return(round(cdf.Percentile(25), 2), round(cdf.Percentile(75), 2))
inter_quart(cdf_pnig)
# random selection from cdf:
cdf_pnig.Random()
# draw and plot random sample as Cdf
n = 1000
sample = cdf_pnig.Sample(n)
random_ranks = [cdf_pnig.PercentileRank(i) for i in sample]
cdf_random = ts2.Cdf(random_ranks)
tplt.Cdf(cdf_random)
# plot PMF of 1000 random values
t = [np.random.random() for _ in range(1000)]
pmf_t = ts2.Pmf(t)
tplt.Pmf(pmf_t, linewidth=0.1)
# assuming PDF does not work very well, plot CDF instead
cdf_t = ts2.Cdf(t)
tplt.Cdf(cdf_t)
# plot difference in percentage points for MAX_AGE between Pinus nigra and all other species around the mean
pnig_pmf = ts2.Pmf(pnig.MAX_AGE)
not_pnig_pmf = ts2.Pmf(not_pnig.MAX_AGE)
ages = np.linspace(50, 80, 31)
diffs = []
for age in ages:
    p1 = pnig_pmf.Prob(age)
    p2 = not_pnig_pmf.Prob(age)
    diff = 100 * (p1 - p2)
    diffs.append(diff)
tplt.Bar(ages, diffs)

# analytic distributions from scipy

# normal distribution
mu = 178 # average height
sigma = 7.7 # standard deviation
dist = scipy.stats.norm(loc=mu, scale=sigma)
type(dist)
# get mean and std from "frozen random variable"
dist.mean(), dist.std()
# how many people are one std below mean?
round(dist.cdf(mu - sigma) * 100., 1)
# between 177.8 and 185.4
round(100 * (dist.cdf(185.4) - dist.cdf(177.8)), 1)

# pareto distribution
alpha = 1.7
xmin = 1.
dist = scipy.stats.pareto(b=alpha, scale=xmin)
# median value
dist.median()
# fraction of people shorter than mean
dist.cdf(dist.mean())
# out of 7 bn people, how many are > 1 km?
(1. - dist.cdf(1000)) * 7e9
# tallest person
dist.sf(600000) * 7e9 # find size to get about one person, here 600 km

# weibull distribution
import random
sample = [random.weibullvariate(2, 1) for _ in range(1000)]
cdf = ts2.Cdf(sample)
tplt.Cdf(cdf, transform='weibull')
# plot percentile ranks of random sample from cdf
def plot_random_percentiles(cdf):
    prs = [cdf.PercentileRank(x) for x in cdf.Sample(1000)]
    pr_cdf = ts2.Cdf(prs)
    tplt.Cdf(pr_cdf)
plot_random_percentiles(cdf)






