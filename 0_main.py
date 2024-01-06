import spotipy
import os 
import numpy as np
import pandas as pd
import yaml
import glob
from spotipy import SpotifyClientCredentials, util
from get_data import Get_data
from clustering import cluster
#from classif_model import clean_df
from classif_model import ML_main
from classif_model import test_prediction


def credentials_spotify():
        
    credentials = yaml.load(open('./credentials.yml'), Loader=yaml.FullLoader)
    client_id = credentials['credentials']['client_id']    
    client_secret = credentials['credentials']['client_secret']
  
    
    # Credentials to access the Spotify music data
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    
# =============================================================================
#     # IF WE CAN ACCESS TO A USER'S PLAYLIST : Credentials to access the playlist's tracks
#     #username = config.username
#     username = credentials['credentials']['username']
#     scope = 'playlist-modify-public'
#     redirect_uri = 'https://example.com'
#     token = util.prompt_for_user_token(username,
#                                scope,
#                                client_id = client_id,
#                                client_secret = client_secret,
#                                redirect_uri = redirect_uri)
#     spt = spotipy.Spotify(auth=token)
# =============================================================================
  
    return sp #, spt


# Create a folder in a specific location in which we can save the results files etc.
def create_dir(path, dirname):
    if not os.path.exists(dirname):
        os.mkdir(path + dirname)  
  



def get_data_per_artist(sp, artist_name, path):

    #create_dir(path, folder)
    create_dir(path, artist_name)
    
    gd = Get_data(artist_name)
    artist_id = gd.get_artist_id(sp)       
    albums_ids_list = gd.get_albums_ids(sp, artist_id, 20)
    tracks_ids_list = gd.get_tracks_ids(sp, albums_ids_list)
    tracks_info_df = gd.get_tracks_info(sp, tracks_ids_list)
    tracks_info_df.to_csv(os.path.join(path+artist_name, f"{artist_name}.csv"))



def artists_data_into_csv(path, folder, filename):
            
    bag = glob.glob(path+folder+'*.csv')        
    artists = []
    for file in bag:
        df = pd.read_csv(file)
        df.reset_index(drop=True, inplace=True)  
        artists.append(df)
    df_art = pd.concat(artists)   
    #df_art = df_art.sample(frac=1, axis=1).reset_index(drop=True)
    df_art.to_csv(path+folder+filename+'.csv')   



def cluster_tracks_csv(path, folder, file_unlabeled, columns_keep, artists_list, file_labeled):
    
    #filepath = path+artist_name+ f'/{artist_name}.csv'
    filepath = path+folder+file_unlabeled+'.csv'
    df = pd.read_csv(filepath, usecols=columns_keep)    
    df_labeled = cluster(df, artists_list)

    #df_labeled.to_csv(os.path.join('./'+artist_name, f"{artist_name}_labels.csv"))
    df_labeled.to_csv(os.path.join(path+folder, f'{file_labeled}.csv'))

    # count labels occurences for aaalll artists (with featuring artists included in an artist album etc)
    #counts = df_labeled.groupby('artist')['label'].value_counts()
    #print(counts)
    
    # count labels occurences for selected artists
    for art in artists_list:
        counts2 = df_labeled[df_labeled['artist']==art].groupby('artist')['label'].value_counts()
        #print(counts2)
        #print('\n')

    
    

# =============================================================================
# WAY TO START :
# Set up Spotify credentials and get access authorisation
# Choose few artists
# Retrieve albums and tracks and informations related
# =============================================================================

if __name__ == "__main__" :
    
    #sp, spt = credentials_spotify()
    sp = credentials_spotify()
    
    #artist_name = input('Artist name : ')
    artist_name = 'Nujabes' #'Donna Summer' #'Boney James' #'Louis Armstrong' #'2pac' #'Slipknot' # 'DJ Okawari' #'Whitney Houston'
    artists_list = ['Boney James', '2Pac', 'Slipknot', 'DJ Okawari', 'Whitney Houston']
    #print(artist_name)
    
    path = './'
    folder = 'artists/'    
    file_labels_NO = 'artists_data_labels_NO'
    file_labels_YES = 'artists_data_labels_YES'
    
    
    # 1) GET TRACKS AND AUDIO FEATURES OF ONE ARTIST INTO .CSV (SPOTIPY)
    #get_data_per_artist(sp, artist_name, path)
    
    
    # 2) GATHER THE ARTISTS' DATA INTO ONE FILE
    #artists_data_into_csv(path, folder, file_labels_NO)
    
    
    # 3) CLUSTER TRACKS BY MOOD    
    columns_keep = ['track_id', 'track_name', 'preview_url', 'artist', 'artist_id', \
                  'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',\
                      'instrumentalness', 'valence', 'tempo'] 
    
    #cluster_tracks_csv(path, folder, file_labels_NO, columns_keep, artists_list, file_labels_YES)


    # 4) BUILD THE MODEL
    model = ML_main(filepath = path+folder+file_labels_YES+'.csv')


    # 5) TEST THE MODEL WITH A SONG
    artist_test_name = 'Nujabes' #'Louis Armstrong'
    song = 'Spiral' #'The Lonesome Road'
    #song = 'West End Blues'
    test_prediction(filepath = path+artist_test_name+'/'+artist_test_name+'.csv', song=song , model=model)
