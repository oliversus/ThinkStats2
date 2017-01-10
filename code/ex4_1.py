import nsfg
import thinkstats2

preg = nsfg.ReadFemPreg()
live = preg[preg.outcome == 1]
live_girls = live[live.babysex == 2]
cdf_live = thinkstats2.Cdf(live.totalwgt_lb)
cdf_live_girls = thinkstats2.Cdf(live_girls.totalwgt_lb)

emilia = 3.14 * 2.20462
cdf_live.PercentileRank(emilia)
cdf_live_girls.PercentileRank(emilia)
