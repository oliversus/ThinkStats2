import brfss
import numpy as np
import thinkstats2
import thinkplot
import nsfg
import matplotlib.pyplot as plt

df = brfss.ReadBrfss(nrows=None)
df = df.dropna(subset=['htm3', 'wtkg2'])
bins = np.arange(135, 210, 5)
indices = np.digitize(df.htm3, bins)
groups = df.groupby(indices)

df_nsfg = nsfg.ReadFemPreg()
df_nsfg = df_nsfg[df_nsfg.outcome==1]
df_nsfg = df_nsfg.dropna(subset=['totalwgt_lb', 'agepreg'])
df_nsfg.totalwgt_lb *= 0.45
# plt.scatter(df_nsfg.totalwgt_lb * 0.45, df_nsfg.agepreg)
# thinkplot.scatter(df_nsfg.totalwgt_lb * 0.45, df_nsfg.agepreg, alpha=0.2)
bins_nsfg = np.arange(10, 45, 2.5)
indices_nsfg = np.digitize(df_nsfg.agepreg, bins_nsfg)
groups_nsfg = df_nsfg.groupby(indices_nsfg)

pearson = thinkstats2.Corr(df_nsfg.agepreg, df_nsfg.totalwgt_lb)
spearman = thinkstats2.SpearmanCorr(df_nsfg.agepreg, df_nsfg.totalwgt_lb)
print("Pearson = " + str(np.round(pearson, 3)) + ", Spearman = " + str(np.round(spearman, 3)))

for i, group in groups_nsfg:
    print(i, len(group))

heights = [group.htm3.mean() for i, group in groups]
ages = [group.agepreg.mean() for i, group in groups_nsfg]
cdfs = [thinkstats2.Cdf(group.wtkg2) for i, group in groups]
cdfs_nsfg = [thinkstats2.Cdf(group.totalwgt_lb) for i, group in groups_nsfg]

for percent in [75, 50, 25]:
    weights = [cdf.Percentile(percent) for cdf in cdfs]
    weights_nsfg = [cdf.Percentile(percent) for cdf in cdfs_nsfg]
    label = '%dth' % percent
    # thinkplot.Plot(heights, weights, label=label)
    thinkplot.Plot(ages, weights_nsfg, label=label)
