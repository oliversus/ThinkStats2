import first
import statsmodels.formula.api as smf
import numpy as np
import regression as rg
import pandas

live, firsts, others = first.MakeFrames()
formula = 'totalwgt_lb ~ agepreg'
model = smf.ols(formula, data=live)
results = model.fit()
inter, slope = results.params['Intercept'], results.params['agepreg']
print(inter, slope)
slope_pvalue = results.pvalues['agepreg']
print(slope_pvalue)
r_squared = results.rsquared
print(r_squared)
# the p-value associated with the model as a whole, similar to testing whether R2 is stat. significant
f_pvalue = results.f_pvalue
print(f_pvalue)
#print(results.summary())
print(np.std(results.resid))
print(np.std(live.totalwgt_lb))

diff_weight = firsts.totalwgt_lb.mean() - others.totalwgt_lb.mean()
diff_age = firsts.agepreg.mean() - others.agepreg.mean()

print(diff_weight, diff_age)

print('========================')
live['isfirst'] = live.birthord == 1
formula = 'totalwgt_lb ~ agepreg + isfirst'
model = smf.ols(formula, data=live)
results = model.fit()
print(results.params)
inter, slope_age = results.params['Intercept'], results.params['agepreg']#, results.params['isfirst']
print(inter, slope)
slope_pvalue = results.pvalues['agepreg']
print(slope_pvalue)
r_squared = results.rsquared
print(r_squared)

# logistic regression
live, firsts, others = first.MakeFrames()
df = live[live.prglngth>30]
df['boy'] = (df.babysex==1).astype(int)
model = smf.logit('boy ~ agepreg', data=df)
results = model.fit()
rg.SummarizeResults(results)

endog = pandas.DataFrame(model.endog, columns=[model.endog_names])
exog = pandas.DataFrame(model.exog, columns=model.exog_names)

formula = 'boy ~ agepreg + hpagelb + birthord + C(race)'
model = smf.logit(formula, data=df)
results = model.fit()
rg.SummarizeResults(results)

actual = endog['boy']
baseline = actual.mean()
predict = (results.predict() >= 0.5)
true_pos = predict * actual
true_neg = (1 - predict) * (1 - actual)
# prediction for new child
columns = ['agepreg', 'hpagelb', 'birthord', 'race']
new = pandas.DataFrame([[35, 39, 3, 2]], columns=columns)
y = results.predict(new)