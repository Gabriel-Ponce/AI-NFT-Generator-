import numpy as np
import pandas as pd


class RankingClassifier: 
"""
Class made to Classify the nfts ranking into 5 rankings sorting them by the amount of money they've made 
"""
    def __init__(self):
        self.nftcsv = pd.read_csv('NFT_Top_Collections.csv')
        
        self.nftcsv.to_csv('test.csv')

        
        #print(self.nftcsv.head())

       
        #print(type(self.nftcsv))

        print("----------------------")
         
        #print(self.nftcsv)
    
    def generateCSVs(self, parts):
         """
        Generate the csv with a certain number of partitions
        
        :args parts: Number of Partitions
        """
        
        self.partitions = parts
        self.nftcsvs = np.array_split(self.nftcsv, self.partitions)
        print(self.nftcsvs)

        for i in range(self.partitions):
            self.nftcsvs[i].to_csv(f'{str(i+1)}.csv', index=False)

            


rankingclassifier = RankingClassifier()
rankingclassifier.generateCSVs(5)




        
