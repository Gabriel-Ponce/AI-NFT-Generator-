import tensorflow_datasets as tfds
import numpy as np
import os
import PIL
#from PIL import Image
from random import randrange
import tensorflow as tf
import pathlib
import glob
from matplotlib import pyplot as plt
import tensorflow_hub as hub
import imageio
from IPython import display
import time
import pathlib

 
class NFT_Generator:
    def __init__(self):
        self.batch_size = 16
        self.img_h = 64
        self.img_w = 64
        self.generator_optimizer = tf.keras.optimizers.Adam(1e-4)
        self.discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)
        self.cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        self.noisedim = 100
        self.g_seed = tf.random.normal([20, self.noisedim])
        self.generator = self.generateImages()
        self.discriminator = self.discriminateImages()
        #self.dataset_url = "/content/drive/MyDrive/NFT_IMAGES.tgz"
        #self.archive = tf.keras.utils.get_file(origin=self.dataset_url, extract=True)
        #print(self.archive)
        #self.data_dir = pathlib.Path(self.archive).with_suffix('')

        
        
        #self.biggangen = hub.Module('https://tfhub.dev/deepmind/biggan-deep-256/1')
        #self.truncation = 0.5  # scalar truncation value in [0.0, 1.0]
        #self.z = self.truncation * tf.random.truncated_normal([self.batch_size, 128])  # noise sample
        #self.y_index = tf.random.uniform([self.batch_size], maxval=1000, dtype=tf.int32)
        #self.y = tf.one_hot(self.y_index, 1000)  # one-hot ImageNet label
        


    def prepareDataset(self):
        """
        Pre-process the data before creating the final generation model
        
        :returns: The NFT Images dataset (Batch Dataset)
        """


        traindataset = tf.keras.utils.image_dataset_from_directory(
            '/content/drive/MyDrive/NFT_IMAGES',
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(self.img_h, self.img_w),
            batch_size= self.batch_size
            )

        print(traindataset)
        class_names = traindataset.class_names
        print(class_names)

        validationdataset = tf.keras.utils.image_dataset_from_directory(
            '/content/drive/MyDrive/NFT_IMAGES',
            validation_split=0.2,
            subset='validation',
            seed= 123,
            image_size=(self.img_h, self.img_w),
            batch_size= self.batch_size,

        )
        
        normalization_layer = tf.keras.layers.Rescaling(1./255)
        
        traindataset.map(lambda x,y: (normalization_layer(x), y))
        validationdataset.map(lambda x,y: (normalization_layer(x), y))

        #AUTOTUNE = tf.data.AUTOTUNE
        #traindataset = traindataset.cache().prefetch(buffer_size = AUTOTUNE)         
       #validationdataset = validationdataset.cache().prefetch(buffer_size = AUTOTUNE)  

        return traindataset
    
        

    
    
    
    def generateImages(self):
        """
        Generate Image from an random noise to then pass it to a discriminator to evaluate the image
        :param z: Noise that will be used to generate the image
        :returns: The 256x256 image generated by the neural network
        """
        
        #dataset = self.prepareDataset()
        
        generator = tf.keras.Sequential()
        generator.add(tf.keras.layers.Dense(16*16*64*3, use_bias=False, input_shape= (100,)))
        generator.add(tf.keras.layers.BatchNormalization())
        generator.add(tf.keras.layers.LeakyReLU())
        generator.add(tf.keras.layers.Reshape((16,16,64*3)))
        assert generator.output_shape == (None, 16, 16, 64*3)
        
        generator.add(tf.keras.layers.Conv2DTranspose(32*3, (5,5), strides=(1,1), padding='same', use_bias=False))
        assert generator.output_shape == (None, 16, 16, 32*3)
        generator.add(tf.keras.layers.BatchNormalization())
        generator.add(tf.keras.layers.LeakyReLU())
        
        generator.add(tf.keras.layers.Conv2DTranspose(16*3, (5,5), strides=(2,2), padding='same', use_bias=False))
        assert generator.output_shape == (None, 32, 32, 16*3)
        generator.add(tf.keras.layers.BatchNormalization())
        generator.add(tf.keras.layers.LeakyReLU())
        
        generator.add(tf.keras.layers.Conv2DTranspose(3, (5,5), strides=(2,2), padding='same', use_bias=False))
        assert generator.output_shape == (None, 64, 64, 3)
        #noise = z
        #generated_image = generator(noise, training=False)
        #print(generated_image)
        #print('------------------------------------')
        #print(generated_image[0])
        #plt.imshow(generated_image[0, :, :, 0], interpolation='nearest')
        #plt.show()

        return generator
    
    def generator_loss(self, fake_output):
        return self.cross_entropy(tf.ones_like(fake_output), fake_output)


    def discriminateImages(self):
        """
        Evaluate how similar the image generated by the generator function is to a dataset
        :returns: The discriminator Sequential Model
        """
        discriminator = tf.keras.Sequential()
        discriminator.add(tf.keras.layers.Conv2D(64, (5, 5), strides=(2, 2), padding='same',input_shape=[64, 64, 3]))
        discriminator.add(tf.keras.layers.LeakyReLU())
        discriminator.add(tf.keras.layers.Dropout(0.3))
        discriminator.add(tf.keras.layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same'))
        discriminator.add(tf.keras.layers.LeakyReLU())
        discriminator.add(tf.keras.layers.Dropout(0.3))
        discriminator.add(tf.keras.layers.Flatten())
        discriminator.add(tf.keras.layers.Dense(1))
        return discriminator

    def discriminator_loss(self, real_output, fake_output):
        """
        Discriminator Loss Function
        """
        real_loss = self.cross_entropy(tf.ones_like(real_output), real_output)
        fake_loss = self.cross_entropy(tf.zeros_like(fake_output), fake_output)
        total_loss = real_loss + fake_loss
        return total_loss
    

    @tf.function
    def train_step(self, images):
        noise = tf.random.normal([self.batch_size, self.noisedim])

        with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
            generated_images = self.generator(noise, training = True)
            print(images[0])
            print(generated_images)
            real_output = self.discriminator(images[0], training = True)
            fake_output = self.discriminator(generated_images, training = True)
            print(real_output)
            gen_loss = self.generator_loss(fake_output)
            disc_loss = self.discriminator_loss(real_output, fake_output)
            print(gen_loss)

        gradients_of_generator = gen_tape.gradient(gen_loss, self.generator.trainable_variables)
        gradients_of_discriminator = disc_tape.gradient(disc_loss, self.discriminator.trainable_variables)
        
        self.generator_optimizer.apply_gradients(zip(gradients_of_generator, self.generator.trainable_variables))
        self.discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, self.discriminator.trainable_variables))

    def train(self, dataset, epochs):
        i = 1
        j = 1
        for epoch in range(epochs):
          start = time.time()
          print(f'Epoch {epoch}')
          i += 1
          print(len(dataset))

          for image_batch in dataset:
            print(f'Batch {j}')
            j+=1
            self.train_step(image_batch)
            if (j==5):
                break

        # Produce images for the GIF as you go
        display.clear_output(wait=True)
        self.generate_and_save_images(self.generator,
                                   epoch + 1,
                                   self.g_seed)



        print ('Time for epoch {} is {} sec'.format(epoch + 1, time.time()-start))

        # Generate after the final epoch
        display.clear_output(wait=True)
        self.generate_and_save_images(self.generator,
                           epochs,
                           self.g_seed)
    def generate_and_save_images(self, model, epoch, test_input):
        predictions = model(test_input, training=False)

        fig = plt.figure(figsize=(4, 4))

        for i in range(predictions.shape[0]):
            #plt.subplot(4, 4, i+1)
            plt.imshow(predictions[i, :, :, 0], interpolation="nearest")
            plt.axis('off')

        plt.savefig('image_at_epoch_{:04d}.png'.format(epoch))
        plt.show()



  

nftgenerator = NFT_Generator()
#dataset = nftgenerator.prepareDataset()
noise = tf.random.normal([1,100])
#print("-"*100)
#print(noise)
#generatedimage = nftgenerator.generateImages(noise)
#discriminator = nftgenerator.discriminateImages()
#discrimination = discriminator(generatedimage)
#print(discrimination)
nftgenerator.train(nftgenerator.prepareDataset(), 1)