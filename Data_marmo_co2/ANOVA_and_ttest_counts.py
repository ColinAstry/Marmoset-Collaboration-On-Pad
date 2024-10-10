import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.anova import AnovaRM
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Read the data from the Excel file
import scipy.stats as stats

df = pd.read_excel(r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\concise0\analysis\2024-05-26_butcounts.xlsx')

# Convert the 'ID' and 'experiment' columns to categories
df['ID'] = df['id'].astype('category')
df['Date'] = df['date'].astype('category')

# #permutation测试
# # Number of times to sample
# num_samples = 1000

# # Initialize a list to store the sampled 'average2' values
# samples = []

# # Randomly select an 'average2' value for each ID and store it in the samples list
# for _ in range(num_samples):
#     sample = df.groupby('ID', observed=False)['average2'].apply(lambda x: x.sample(n=1, replace=True)).values
#     samples.extend(sample)

# # Calculate the 2.5th and 97.5th percentiles of the samples
# conf_int_low = np.percentile(samples, 2.5)
# conf_int_high = np.percentile(samples, 97.5)

# print(f'Confidence interval: ({conf_int_low}, {conf_int_high})')

# # Add a new column to the dataframe indicating whether each day's 'average2' value is within the confidence interval
# df['in_conf_int'] = df['average2'].apply(lambda x: conf_int_low <= x <= conf_int_high)

# # Select only the columns of interest
# df = df[['Date', 'ID', 'average2', 'in_conf_int']]

# # Print the dataframe
# print(df)


# # Number of times to sample
# num_samples = 1000

# # Get the unique IDs
# ids = df['ID'].unique()

# # Initialize a dictionary to store the confidence intervals for each ID
# conf_ints = {}

# # For each ID, randomly select an 'average2' value num_samples times and calculate the confidence interval
# for id in ids:
#     means = []
#     for _ in range(num_samples):
#         sample = df.loc[df['ID'] == id, 'average2'].sample(n=len(df.loc[df['ID'] == id, 'average2']), replace=True)
#         means.append(sample.mean())
#     conf_int_low = np.percentile(means, 2.5)
#     conf_int_high = np.percentile(means, 97.5)
#     conf_ints[id] = (conf_int_low, conf_int_high)
#     print(f'Bootstrap confidence interval for mean of ID {id}: ({conf_int_low}, {conf_int_high})')

# # Add a new column to the dataframe indicating whether each day's 'average2' value is within the confidence interval for its ID
# df['in_conf_int'] = df.apply(lambda row: conf_ints[row['ID']][0] <= row['average2'] <= conf_ints[row['ID']][1], axis=1)

# # Select only the columns of interest
# df = df[['Date', 'ID', 'average2', 'in_conf_int']]

# # Print the dataframe
# print(df)



# # Aggregate the data by calculating total/sum(max_t0) for each combination of 'ID' and 'experiment'
# df_agg = df.groupby(['ID', 'experiment']).apply(lambda group: pd.Series({
#     'average': group['total'].sum() / group['max_t0'].sum()
# })).reset_index()
# # Perform the repeated measures ANOVA
# anova = AnovaRM(df_agg, 'average', 'ID', within=['experiment'])
# res = anova.fit()
# print(res)

#t检验
# from scipy.stats import ttest_ind

# # Select the data for the two subjects
# subject1_data = df[df['id'] == 723]['average2']
# subject2_data = df[df['id'] == 772]['average2']

# print(len(subject1_data))
# print(len(subject2_data))
# print(df['ID'].unique())

# # Perform the t-test
# t_stat, p_value = ttest_ind(subject1_data, subject2_data)

# print(f'T-statistic: {t_stat}')
# print(f'P-value: {p_value}')

# # Create a figure with two subplots
# fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# # Plot the histogram of subject1_data
# sns.histplot(subject1_data, kde=True, ax=axs[0])
# axs[0].set_title('Subject 1')

# # Plot the histogram of subject2_data
# sns.histplot(subject2_data, kde=True, ax=axs[1])
# axs[1].set_title('Subject 2')

# # Show the plot
# plt.tight_layout()
# plt.show()

# # Exclude rows where 'date' does not have a pair
# df = df.groupby('date').filter(lambda group: len(group) > 1)

# # Perform the repeated measures ANOVA
# anova = AnovaRM(df, 'average', 'ID', within=['date'])
# res = anova.fit()

# print(res)

# #可能应该用多层线性模型？
# import statsmodels.formula.api as smf

# # Fit the multilevel model
# model = smf.mixedlm("average ~ experiment", df, groups=df['ID'])
# result = model.fit()

# print(result.summary())

# import statsmodels.formula.api as smf
# from scipy.stats import chi2

# # Fit the mixed model
# mixed_model = smf.mixedlm("average ~ experiment", df, groups=df['ID']).fit(reml=False)

# # Fit the linear regression model
# linear_model = smf.ols("average ~ experiment", df).fit()

# # Perform the likelihood ratio test
# lr_stat = -2 * (linear_model.llf - mixed_model.llf)
# p_value = chi2.sf(lr_stat, df=1)

# print(f'Likelihood ratio statistic: {lr_stat}')
# print(f'P-value: {p_value}')