from PIL import Image
import os, sys
import time

path = f"C:/Users/ponce/OneDrive/Documentos/Workspace/Python/AI NFT Generator/NFT_IMAGES/{sys.argv[1]}/"
dirs = os.listdir(path)

def resize():
    """
    Resize all the nfts retrieved from the api to 128x128 to be able to feed them into the AI model
    """
    for item in dirs:
            try:
                print(item)
                im = Image.open(path + item)
                imResize = im.resize((128, 128))
                imResize.save(path + item)
            except:
                print(item + ' failed to resize\nDeleting Image....')
                os.system(f'del /f "{path + item}"')
                time.sleep(4)

resize()