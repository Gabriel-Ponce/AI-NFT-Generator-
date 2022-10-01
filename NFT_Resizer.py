from PIL import Image
import os, sys
import time

path = f"C:/Users/ponce/OneDrive/Documentos/Workspace/Python/AI NFT Generator/NFT_IMAGES/{sys.argv[1]}/"
dirs = os.listdir( path )

def resize():
    for item in dirs:
            try:
                print(item)
                im = Image.open(path + item)
                imResize = im.resize((512, 512))
                imResize.save(path + item)
            except:
                print(item + ' failed to resize')
                time.sleep(800)

resize()