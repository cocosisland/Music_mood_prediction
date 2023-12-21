import numpy as np
import pandas as pd
pd.set_option("display.max_columns", None)
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans


# K-Means Clustering Algorithm


def optimal_k(Sum_of_squared_distances):
    x = range(1, 15)
    y = Sum_of_squared_distances
    plt.plot(x,y)
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title("Elbow method for optimal k")
    plt.show()

    
def cluster(df):
    
    print(df.shape)  # (231, 11)

    scaler = MinMaxScaler()
    df['loudness_scaled'] = scaler.fit_transform(df[['loudness']])
    #print(df['loudness_scaled'])


    features_cols = ['danceability', 'energy', 'loudness_scaled', 'speechiness', 'acousticness',\
                      'instrumentalness', 'valence']
    
    df_features = df[df.columns.intersection(features_cols)]
    print(df_features.shape)
    print(type(df_features))
    
    
    # Search for the optimal K       - pip install threadpoolctl --upgrade
    Sum_of_squared_distances = []
    K = range(1,15)
    for k in K:
        km = KMeans(n_clusters = k)
        km = km.fit(df_features)
        Sum_of_squared_distances.append(km.inertia_)
        
        
    print(Sum_of_squared_distances)    
# =============================================================================
# [66.0998554254598, 33.156726964896286, 28.474052198243207, 24.154368956230655, 
#  21.5357941472274, 19.814870202993276, 17.85359748580357, 16.03710916218415, 
#  14.96126655248069, 14.037825444950432, 13.35277304124485, 12.53941424106372, 
#  11.680885849406632, 11.381927024339706] 
# =============================================================================

    # plot graph to find k
#    optimal_k(Sum_of_squared_distances)    # ------> Optimal k = 4


    kmeans = KMeans(n_clusters = 4)
    kmeans.fit(df_features)
    y_km = kmeans.predict(df_features)
    
# =============================================================================
# plt.scatter(df_features[:, 0], df_features[:, 1], c=y_km, s=50, cmap='viridis')
# 
# centers = km.cluster_centers_
# plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5);    
# =============================================================================

    
    labels = KMeans(4, random_state=0).fit_predict(df_features)
    plt.scatter(df_features[:, 0], df_features[:, 1], c=labels, s=50, cmap='viridis');

   
