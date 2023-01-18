import numpy as np
import tensorflow as tf
import tensorflow_hub as hub


batch_size = 32
biggangen = hub.Module('https://tfhub.dev/deepmind/biggan-deep-256/1')
truncation = 0.5  # scalar truncation value in [0.0, 1.0]
z = truncation * tf.random.truncated_normal([batch_size, 128])  # noise sample
y_index = tf.random.uniform([batch_size], maxval=1000, dtype=tf.int32)
y = tf.one_hot(y_index, 1000)  # one-hot ImageNet label