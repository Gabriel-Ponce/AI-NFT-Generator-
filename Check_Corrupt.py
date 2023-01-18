from os import listdir
import cv2
import sys 

path = f"C:/Users/ponce/OneDrive/Documentos/Workspace/Python/AI NFT Generator/NFT_IMAGES/{sys.argv[1]}"
dirs = listdir(path)
#for filename in listdir('C:/tensorflow/models/research/object_detection/images/train'):
for filename in listdir(path):
  if filename.endswith(".png"):
    print(filename)
    #cv2.imread('C:/tensorflow/models/research/object_detection/images/train/'+filename)
    cv2.imread(path+filename)