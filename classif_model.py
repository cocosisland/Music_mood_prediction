import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay
#Libraries to create the Multi-class Neural Network
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils#Import tensorflow and disable the v2 behavior and eager mode
import tensorflow as tf
tf.compat.v1.disable_eager_execution()
tf.compat.v1.disable_v2_behavior()

from sklearn.preprocessing import MinMaxScaler




def clean_df(filepath):
    
    df = pd.read_csv(filepath)
    
    # drop unnecessary columns
    df.drop(columns=['Unnamed: 0', 'track_id', 'track_name', 'preview_url', 'artist', \
                     'artist_id', 'loudness', 'tempo'], inplace=True)

    # define the features and the target
    col_features = df.columns[1:]
    X = df[col_features]
    Y = df['label']
    
    return X, Y



def split_dataset(X, Y, test_size, random_state):
    
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=random_state)

    return X_train, X_test, Y_train, Y_test



# function that creates the structure of the Neural Network
def create_model():
    
    # create model
    model = Sequential() 
    model.add(Dense(8, input_dim=8, activation='relu'))  
    model.add(Dense(4, activation='softmax'))
    
    # compile the model using logistic loss function and adam optimizer, accuracy correspond to the metric displayed
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
   
    return model



def train_model(X_train, Y_train, X_test, Y_test):
    
    # configure the estimator with 300 epochs and 200 batchs. the build_fn takes the function defined above.
    model = KerasClassifier(build_fn= create_model, epochs=300, batch_size=200)    

# =============================================================================
#     # evaluate using 10-fold cross validation
#     kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
#     results = cross_val_score(model, X, Y, cv=kfold)
#     print(results.mean())
# =============================================================================
    
    # train model
    model.fit(X_train, Y_train)
    
    # predict model with test data
    y_preds = model.predict(X_test)
    #y_preds = np.argmax(model.predict(X_test), axis=-1)
    
    
    print(y_preds)

    conf_matrix = confusion_matrix(Y_test, y_preds)
    print(conf_matrix)


    # plot Confusion matrix
    fig, ax = plt.subplots(figsize=(8,6), dpi=100)
    display = ConfusionMatrixDisplay(conf_matrix, display_labels=model.classes_)
    ax.set(title='Confusion matrix of the Music moods')
    display.plot(ax=ax);

    return model



def test_prediction(filepath, song, model):
    
    df = pd.read_csv(filepath)
    
    scaler = MinMaxScaler()
    df['loudness_scaled'] = scaler.fit_transform(df[['loudness']])
    df['tempo_scaled'] = scaler.fit_transform(df[['tempo']])
    
    song = df.loc[df['track_name'] == song]
    
    features_cols = ['danceability', 'energy', 'loudness_scaled', 'speechiness', 'acousticness',\
                      'instrumentalness', 'valence', 'tempo_scaled']
    
    X_song = song[song.columns.intersection(features_cols)]
    print(X_song)

    
    y_pred = model.predict(X_song)
    #y_pred = np.argmax(model.predict(X_song), axis=-1)

    print('\n\n')
    print(y_pred)
    
    
    
def ML_main(filepath):

    X, Y = clean_df(filepath)
    X_train, X_test, Y_train, Y_test = split_dataset(X, Y, test_size=0.2, random_state=42)
    print(X_test)
    #print(len(X_train.columns))
    model = train_model(X_train, Y_train, X_test, Y_test)        
    
    return model


