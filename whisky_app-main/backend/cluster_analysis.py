# %%
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

# %%
df = pd.read_csv('./dataset/whiskies_b.csv')
flavours = ['Body','Sweetness','Smoky','Medicinal', 'Tobacco', 'Honey', 'Spicy', 'Winey', 'Nutty', 'Malty', 'Fruity', 'Floral']

for k in range(2,15):
    
    # Run the Kmeans algorithm
    km = KMeans(n_clusters=k)
    labels = km.fit_predict(df[flavours])
    
    # Get silhouette samples
    score = silhouette_score(df[flavours], labels)
    print(f'k:{k} score:{score} ')
# # %%
# # Elbow Method: search for 
sse = []
list_k = list(range(1,19))

for k in list_k:
    km = KMeans(n_clusters=k)
    km.fit(df[flavours])
    sse.append(km.inertia_) ## the sum of squared distance (SSE) between data points and their assigned clusters’ centroids.

# # Plot sse against k
plt.figure(figsize=(6, 6))
plt.plot(list_k, sse, '-o')
plt.xlabel(r'Number of clusters *k*')
plt.ylabel('Sum of squared distance')
# %%
# PCA
from sklearn.decomposition import PCA
pca = PCA()
X = pca.fit(df[flavours])
explained_variance = pca.explained_variance_ratio_ 
count = 1
total = 0
# print accumulative explained variance by components
for i in explained_variance:
    total += i
    print(str(count) + "-component: " + str(round(total*100, 2)) + "% variance explained")
    count += 1
# %%
total = 0
for i in explained_variance:
    total = total + i
    print(total)
# # %%

fig = plt.figure(1, figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)
X_reduced = PCA().fit_transform(df[flavours])
ax.scatter(X_reduced[:, 0], X_reduced[:, 1], X_reduced[:, 2], edgecolor='k')
ax.set_title("First three PCA directions")
ax.set_xlabel("1st eigenvector")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("2nd eigenvector")
ax.w_yaxis.set_ticklabels([])
ax.set_zlabel("3rd eigenvector")
ax.w_zaxis.set_ticklabels([])
# %%
