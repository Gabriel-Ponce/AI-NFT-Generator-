import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras



class RankingClassifier: 

    def __init__(self):
        self.nftcsv = pd.read_csv('NFT_Top_Collections.csv')
        

        self.nftcsv.pop('Name')

        self.nftcsv[
        ['Index', 'Volume', 'Market_Cap', 'Market_Cap_USD', 'Sales', 'Volume_USD',
        'Floor_Price', 'Floor_Price_USD', 'Average_Price', 'Average_Price_USD', 'Owners', 'Assets', 
        'Owner_Asset_Ratio']] = self.nftcsv[
        ['Index', 'Volume', 'Market_Cap', 'Market_Cap_USD', 'Sales', 'Volume_USD',
        'Floor_Price', 'Floor_Price_USD', 'Average_Price', 'Average_Price_USD', 'Owners', 'Assets', 
        'Owner_Asset_Ratio']].astype(np.float32)        
       
        #print(self.nftcsv.head())
        
        self.nftcsv.to_csv('test.csv')

        self.value = self.nftcsv.pop('Volume_USD')

        #print(type(self.nftcsv))
        
        for i in range(3):
            self.nftcsv.drop(columns = self.nftcsv.columns[-1], axis = 1, inplace = True)
        print(self.nftcsv.head())

        #self.nftcsv = self.nftcsv.fillna(value='', inplace=True)
        

    def buildModel(self, epochs = 10):

        self.tr_data = np.asmatrix(self.nftcsv)
        
        self.tr_data = [self.tr_data]

        print (self.tr_data)

        self.tr_data = tf.convert_to_tensor(self.tr_data, dtype=tf.float32)

        

        self.tr_labels = np.asmatrix(self.value)
        self.tr_labels = tf.convert_to_tensor(self.tr_labels, dtype=tf.float32)



        self.model = tf.keras.Sequential([tf.keras.layers.Flatten(),
        tf.keras.   layers.Dense(128, activation=tf.nn.relu), 
        tf.keras.layers.Dense(15, activation=tf.nn.relu),
        tf.keras.layers.Dense(5, activation=tf.nn.softmax)])


        self.model.compile(optimizer = tf.optimizers.Adam(), loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])

        self.model.fit(self.tr_data, self.tr_labels, epochs=epochs)

        #print(f'value: {self.value[5]}')
        #print(self.nftcsv.head())
        #print(max(self.nftcsv['Volume']))
        
        



rankingclassifier = RankingClassifier()
rankingclassifier.buildModel()




        
