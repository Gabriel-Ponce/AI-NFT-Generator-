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

dataset = list(glob.glob('NFT_IMAGES/1/*.png'))
print(len(dataset))
IS = (512, 512)
image = PIL.Image.open(dataset[randrange(410)]).resize(IS)
image.show()

module = hub.load('https://tfhub.dev/deepmind/biggan-deep-512/1')

a = module(image)

print(a)


