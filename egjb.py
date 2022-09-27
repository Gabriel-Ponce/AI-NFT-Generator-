import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

# Load BigGAN 512 module.
module = hub.load('https://tfhub.dev/deepmind/biggan-512/2')

# Sample random noise (z) and ImageNet label (y) inputs.
batch_size = 8
truncation = 0.5  # scalar truncation value in [0.02, 1.0]
z = truncation * tf.random.truncated_normal([batch_size, 128])  # noise sample
y_index = tf.random.uniform([batch_size], maxval=1000, dtype=tf.int32)
y = tf.one_hot(y_index, 1000)  # one-hot ImageNet label

# Call BigGAN on a dict of the inputs to generate a batch of images with shape
# [8, 512, 512, 3] and range [-1, 1].
samples = module(y=y, z=z, truncation=truncation)

print(samples)