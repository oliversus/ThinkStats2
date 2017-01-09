import thinkstats2
import thinkplot
import nsfg
import math

preg = nsfg.ReadFemPreg()
live = preg[preg.outcome == 1]

# hist = thinkstats2.Hist(live.birthwgt_lb, label='birthwgt_lb')
# thinkplot.Hist(hist)
# thinkplot.Show(xlabel='pounds', ylabel='frequency')

# hist = thinkstats2.Hist(live.agepreg, label='agepreg')
# thinkplot.Hist(hist)
# thinkplot.Show(xlabel='age', ylabel='frequency')

hist = thinkstats2.Hist(live.prglngth, label='prglngth')
# thinkplot.Hist(hist)
# thinkplot.Show(xlabel='weeks', ylabel='frequency')

# for weeks, freq in hist.Smallest(10):
#     print(weeks, freq)

# for weeks, freq in hist.Largest(10):
#     print(weeks, freq)

firsts = live[live.birthord == 1]
others = live[live.birthord != 1]

first_hist = thinkstats2.Hist(firsts.prglngth)
other_hist = thinkstats2.Hist(others.prglngth)

width = 0.45
thinkplot.PrePlot(2)
thinkplot.Hist(first_hist, align='right', width=width)
thinkplot.Hist(other_hist, align='left', width=width)
# thinkplot.Show(xlabel='weeks', ylabel='frequency',
#                xlim=[27, 46])

def CohenEffectSize(group1, group2):
    diff = group1.mean() - group2.mean()
    var1 = group1.var()
    var2 = group2.var()
    n1, n2 = len(group1), len(group2)
    pooled_var = (n1 * var1 + n2 * var2) / (n1 + n2)
    d = diff / math.sqrt(pooled_var)
    return d

a = firsts.prglngth.mean()
b = others.prglngth.mean()
print a, b

cohen_length = CohenEffectSize(firsts.prglngth, others.prglngth)
print cohen_length

a = firsts.totalwgt_lb.mean()
b = others.totalwgt_lb.mean()
print a, b

cohen_weight = CohenEffectSize(firsts.totalwgt_lb, others.totalwgt_lb)
print cohen_weight

