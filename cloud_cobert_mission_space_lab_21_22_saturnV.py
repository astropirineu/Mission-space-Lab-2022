# Mission Space Lab 2022 - Saturn V
# Institut Pere Borrell
# Puigcerdà - Spain 

from pathlib import Path  
import matplotlib.pyplot
from PIL import Image
import numpy as numpy
import csv
import matplotlib
import matplotlib.pyplot as plt
import gc
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
matplotlib.use('Agg')

#Set a work path // Escollim el directori de treball
base_folder = Path(__file__).parent.resolve()
#We have a template to define the work area where we will count the cloud cover
plantilla = Path(base_folder,"plantilla_negre_blanc_saturnV.png")
imgp = Image.open(plantilla)
imgpR, imgpG, imgpB , imgpA = imgp.split()
arrpR = numpy.asarray(imgpR).astype('float')
# arrpB = numpy.asarray(imgpB).astype('float')
# arrpG = numpy.asarray(imgpG).astype('float')

#We want that the template to have 0 or 1
arrpR[arrpR !=0.0] = 1.0
# arrpG[arrpG !=0.0] = 1.0
# arrpB[arrpB !=0.0] = 1.0

# Open data file and write header for counter, photo name, percentage of clouds
# and limit value to determine the interval clouds
def create_csv_file(data_file):
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Counter", "Nom", "Núvols" , "Límit")
        writer.writerow(header)
# Put down the information : counter, photo name, percentage of clouds, limit intensity value for the clouds
def add_csv_data(data_file, data):
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

data_file=Path(base_folder,"results/percentatges220_220.csv")
create_csv_file(data_file)
ini = 220
while ini<221:
    numFoto = str(ini)
    fileFormat1 = ".jpg"
    fileFormat2 = ".jpg"
    nom="foto_saturnV_" + numFoto + fileFormat1
    image = Path(base_folder,nom)
    print(image)
    nom="results/saturnV_RGB_ini_" + numFoto + fileFormat2
    imageOut0 = Path(base_folder,nom)
    nom="results/saturnV_RGB_" + numFoto + fileFormat2
    imageOut = Path(base_folder,nom)
    nom="results/saturnV_RGBnuvols_" + numFoto + fileFormat2
    imageOut2 = Path(base_folder,nom)
    # We open the image to analyze
    img = Image.open(image)
    print("img",img)
    
    # We get 3 channels R, G, B
    imgR, imgG, imgB = img.split()
   
    # We pass the values of 3 images to float 
    arrR = numpy.asarray(imgR).astype('float')
    arrB = numpy.asarray(imgB).astype('float')
    arrG = numpy.asarray(imgG).astype('float')

    # We apply the template multiplying both images
    arrRxp = arrR * arrpR
    arrGxp = arrG * arrpR
    arrBxp = arrB * arrpR

    # We set the lower limit for the cloud intensity interval
    limit = 180.
    # We create the image in one channel where we assume the clouds must have the maximum intensity level
    arrRGB = (arrRxp + arrGxp + arrBxp) / 3.0 
    arrselect = arrRGB.copy()
    print(arrselect)
    # We put the clouds intensity to 50 and the rest of the image corresponds ro (R+G+B)/3
    arrselect[arrselect >= limit] = 50.0
    
    # For better visualitzation, we paint the clouds over the original image
    arrselect2 = arrselect.copy()
    # We pass to integer to be able to compare with a integer
    arrselect = numpy.asarray(arrselect).astype('int')
    # We modify the original channels with the blue color (0,0,255) for the clouds
    numpy.putmask(arrR,  arrselect == 50, 0.0)
    numpy.putmask(arrG,  arrselect == 50, 0.0)
    numpy.putmask(arrB,  arrselect == 50, 255.0)
    
    # We convert the modified images to 8bit images 
    arrR = numpy.asarray(arrR).astype('uint8')
    arrG = numpy.asarray(arrG).astype('uint8')
    arrB = numpy.asarray(arrB).astype('uint8')
    
    
    nouarrR = Image.fromarray(arrR, mode="L")
    nouarrG = Image.fromarray(arrG, mode="L")
    nouarrB = Image.fromarray(arrB, mode="L")
    
    #We turn to the original image format with painted
    novaRGB = Image.merge("RGB", (nouarrR,nouarrG,nouarrB))
    
    # Controls to track the code
    max_value = numpy.max(arrR)
    min_value = numpy.min(arrR)
    print("max: ", max_value)
    print("min: ", min_value)

    max_value = numpy.max(arrRxp)
    min_value = numpy.min(arrRxp)
    print("max: ", max_value)
    print("min: ", min_value)

    # We savw the images
    
    # Save the image original with clouds painted
    fig = plt.figure(figsize=(16,12))
    im = plt.imshow(novaRGB)
    plt.savefig(imageOut0)
    plt.close()
    
    #Save the (image R+G+B)/3 with nipy_spectral colormap
    fig = plt.figure(figsize=(16,12))
    im = plt.imshow(arrRGB, interpolation='none', vmin=0.0, vmax=255.0)
    im.set_cmap('nipy_spectral')
    fig.colorbar(im)
    plt.savefig(imageOut)
    plt.close()
    
    #Save the image above with the clouds painted
    fig = plt.figure(figsize=(16,12))
    im2 = plt.imshow(arrselect,interpolation='none',vmin=0.0, vmax=255.0)
    im2.set_cmap('nipy_spectral')
    #fig.colorbar(im2)
    plt.savefig(imageOut2)
    
    # Area for the field of view. The two quantities are equal if all goes well
    npixelsplantilla = (arrpR !=0.0).sum()
    npixelstot = (arrRGB != 0.0).sum()
    
    # Area for the clouds
    npixelsnuv = (arrRGB >= limit).sum()
    #Percentage of clouds
    percentatge=npixelsnuv / npixelstot * 100.0
    
    #Controls to track the code
    print ("Pixelsplantilla: ", npixelsplantilla)
    print ("Pixelsutils: ", npixelstot)
    print("nuvols: ", npixelsnuv * 1.0)
    print("% nuvols: ", npixelsnuv / npixelstot * 100.0 )
    print("valor del pixel del mig: ", arrRxp[2045,1520])
    
    # We write the percentage results on file
    data = (ini,image,percentatge,limit)
    add_csv_data(data_file, data)
    
    #We release memory
    del arrR
    del arrB
    del arrG
    del arrRxp
    del arrGxp
    del arrBxp
    del arrselect
    del arrselect2
    del arrRGB
    del nouarrR
    del nouarrG
    del nouarrB
    del novaRGB
   
    gc.collect()
    
    # To another image
    ini +=1


