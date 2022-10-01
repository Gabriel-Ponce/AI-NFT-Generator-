import numpy as np
import pandas as pd
import json
import requests
import os
from io import BytesIO
from random import randrange
from opensea import OpenseaAPI
from googleapiclient.discovery import build
from PIL import Image
import sys

class NFT_Retriever:
"""
This class Retrieves NFT's using curl to access the OpenSea API without having an API KEY
"""
    
    def __init__(self, qual_cat = 1):
        self.category = pd.read_csv(f'{str(qual_cat)}.csv')
        self.api = OpenseaAPI()
        self.test = self.category['Collections'][randrange(50)]
        
        self.APIKEY = 'AIzaSyCr2uc5N089_JIanMbTF14gtsWLCebk5cY'
        self.CLIENT_ID = '50d91505283954384'
        self.category_num = qual_cat

        print(self.test)

    
    def openseaSearch(self, searchterm, **kwargs):
        """
        Use the Google Search API to query the name of a collection and returns the link of the most similar collection
        
        :param searchterm: the collection term to be searched  

        :returns: final part of the collection link
        
        """
        googleapi = build("customsearch" ,"v1", developerKey= self.APIKEY)
        res = googleapi.cse().list(q=searchterm, cx=self.CLIENT_ID, **kwargs).execute()
        try:
        
            link = res['items'][0]['link']
            return link[30:]

        except Exception as e:
            print(e)
            print(res)

    def getCollection(self, collection_index=0):
        """
        Get the Collection name from the csv
        
        :returns: Collection name as a string
        """
        
        return self.category['Collections'][collection_index]
        #print(self.result)
    
    def getAssets(self, collection_name):

        """
        Use the windows command prompt to use curl and get a collection using the openSea API and saves the json as a .json
        file
        
        :param searchterm: the collection term to be searched
        
        """
        
        cmd_command = f'cd {os.getcwd()}/NFTs && curl "https://api.opensea.io/api/v1/assets?collection={collection_name}&format=json&include_orders=false&limit=20&order_direction=desc" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0" -o {collection_name}.json'

        print(cmd_command)
        os.system(cmd_command)
        
    
    def getNFT(self, filename, nft_amount=1):

    
        with open(f'NFTs/{filename}.json') as i_json:
            
            self.nftjson = json.load(i_json)
            

        i = 0
        for i in range(nft_amount):
            print(i)
            
            try:

                nftlink = self.nftjson['assets'][i]['image_url'] 


                if nftlink == 'null':
                    nftlink = self.nftjson['assets'][i+1]['image_url'] 
                    i += 1
                    print('Found a null NFT')

                nft_data = requests.get(nftlink)
                nft_image = Image.open(BytesIO(nft_data.content))
                nft_image.save(f'NFT_IMAGES/{self.category_num}/{filename}_{i}.png')

            except Exception as e:
                print('Asset Error')
                print(e)
                i+=1

    def getRankingNFTS(self): 
        
        for j in range(46):
            j+=1
            try:
                nft_result = self.openseaSearch(self.getCollection(j))
                self.getAssets(nft_result)
                self.getNFT(nft_result, 15)     

            except Exception as e:
                print(e)
                print('Collection Error')
                j+=1   



nftretriever = NFT_Retriever(int(sys.argv[1]))
nftretriever.getRankingNFTS()