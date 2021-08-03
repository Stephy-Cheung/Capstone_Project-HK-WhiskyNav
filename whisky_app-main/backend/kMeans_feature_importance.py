#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
import seaborn as sns
# %matplotlib inline

#%%
#============================== kMeans ==============================
df = pd.read_csv('./dataset/whiskies_b.csv', sep=',')
df = df.drop(['RowID','Distillery','Postcode','Latitude','Longitude','lat','long'], axis=1)

x_train=df
from sklearn.metrics import silhouette_samples, silhouette_score
for k in range(2,11):
    
    # Run the Kmeans algorithm
    km = KMeans(n_clusters=k)
    labels = km.fit_predict(x_train)

    # Get silhouette samples
    score = silhouette_score(x_train, labels)
    print(f'k:{k} score:{score} ')

sse = []
list_k = list(range(1,10))

for k in list_k:
    km = KMeans(n_clusters=k)
    km.fit(df)
    sse.append(km.inertia_) ## the sum of squared distance (SSE) between data points and their assigned clusters’ centroids.

# Plot sse against k
plt.figure(figsize=(6, 6))
plt.plot(list_k, sse, '-o')
plt.xlabel(r'Number of clusters *k*')
plt.ylabel('Sum of squared distance')

#%%
#========= Assume 4 clusters, find the feature importance =========
km = KMeans(n_clusters = 4, random_state=90)
cluster1 = km.fit_predict(df)

scaled_df = preprocessing.StandardScaler().fit_transform(df)

model = LogisticRegression()
model.fit(scaled_df, cluster1)
importance = model.coef_[0]
for i,v in enumerate(importance):
	print('Coefficient:%6.3f, %s' % (v,[j for j in df.columns][i]))

plt.figure(figsize=(10, 10))
sns.heatmap(df.corr(), annot=True)
# %%
