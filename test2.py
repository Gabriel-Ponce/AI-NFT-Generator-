import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from matplotlib import pyplot as plt

# Load BigBiGAN module.

module = tf.keras.Sequential({
hub.KerasLayer('https://tfhub.dev/deepmind/bigbigan-revnet50x4/1')


})



z = tf.random.normal([8, 120]) 
print(z)

gen_samples = module(z, signature='generate')
print(gen_samples)

#images = tf.placeholder(tf.float32, shape=[None, 256, 256, 3])
#features = module(images, signature='encode', as_dict=True)
#print("features \n", features)
#
#z_sample = features['z_sample'] 
#print("z_sample", z_sample)
#
#
#recons = module(z_sample, signature='generate') 
#
#
#print("recons", recons)
#