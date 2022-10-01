#import tensorflow_hub as hub
import numpy as np
import os
import PIL
from PIL import Image
from random import randrange
import tensorflow as tf
import pathlib
import glob
from matplotlib import pyplot as plt


import tensorflow_hub as hub
import numpy as np
import os
import PIL
import PIL.Image
from random import randrange
import tensorflow as tf
import pathlib
import glob
#import tensorflow_datasets as tfds

class NFT_Generator:

    def __init__(self):
        self.batch_size = 32
        self.img_h = 512
        self.img_w = 512

    def prepareDataset(self): 
        traindata = tf.keras.utils.image_dataset_from_directory(
            'NFT_IMAGES',
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(self.img_h, self.img_w),
            batch_size= self.batch_size
            )
        print(traindata)
        class_names = traindata.class_names
        print(class_names)
        
        normalization_layer = tf.keras.layers.Rescaling(1./255)
        #traindata = traindata.map()


nftgenerator = NFT_Generator()
nftgenerator.prepareDataset()        
