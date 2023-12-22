import numpy as np
import pandas as pd
pd.set_option("display.max_columns", None)
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import seaborn as sns
from sklearn.decomposition import PCA 
from sklearn.datasets import make_blobs



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
    
    
    # Search for the optimal K       probably need-> pip install threadpoolctl --upgrade
    Sum_of_squared_distances = []
    K = range(1,15)
    for k in K:
        km = KMeans(n_clusters = k)
        km = km.fit(df_features)
        Sum_of_squared_distances.append(km.inertia_)
        
        
    print(Sum_of_squared_distances)    # list of 15 values


    # plot graph to find k
#    optimal_k(Sum_of_squared_distances)    # ------> Optimal k = 4

    pca = PCA(2)    # dimensionality reduction in 2D. Note: PCA reduces the dimensionality without losing information from any features
    pca_df = pd.DataFrame(pca.fit_transform(df_features), columns=['x','y']) 

    # train a K-Means cluster on the tracks data that will try to find each blob's center
    # and assign each instance to the closest blob.
    kmeans = KMeans(n_clusters = 4).fit(df_features)
    
    pca_df['cluster'] = pd.Categorical(kmeans. labels_)
    sns.scatterplot(x="x", y="y", hue="cluster", data=pca_df)
    
    print(pca_df)

    df.insert(4, 'label', pca_df['cluster'])
    print(df)
    return df
