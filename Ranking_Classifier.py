import numpy as np
import pandas as pd


class RankingClassifier: 

    def __init__(self):
        self.nftcsv = pd.read_csv('NFT_Top_Collections.csv')
        
        self.nftcsv.to_csv('test.csv')

        
        #print(self.nftcsv.head())

       
        #print(type(self.nftcsv))

        print("----------------------")
         
        #print(self.nftcsv)
    
    def generateCSVs(self):
        self.partitions = 5
        self.nftcsvs = np.array_split(self.nftcsv, self.partitions)
        print(self.nftcsvs)

        for i in range(self.partitions):
            self.nftcsvs[i].to_csv(f'{str(i+1)}.csv', index=False)

            


rankingclassifier = RankingClassifier()
rankingclassifier.generateCSVs()




        
