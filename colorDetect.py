import requests
import os
import json
import heapq
import time

def colorDetection(partInfo):
    colors = []
    colorIDs = []
    i = []
    colorConf = []
    finalColor = []
    for i in partInfo['colors']:
        colorIDs.append(i['id'])
        colors.append(i['name'])    
        colorConf.append(i['score'])
    if len(colorIDs) < 1:
        return [None,None]
    if len(colorIDs) > 1:
        highestConfidence = max(colorConf)
        secondHighConf = float(heapq.nlargest(2,colorConf)[1])
        diff = abs(highestConfidence - secondHighConf) / highestConfidence
        firstIndex = colorConf.index(highestConfidence)
        secondIndex = colorConf.index(secondHighConf)
        return [colorIDs[firstIndex],colors[firstIndex]]
        #if within 20%, show one which one to save
        if diff <= (.20):
            choice = int(input("Part IDs: "+str(colorIDs[firstIndex])+", "+str(colorIDs[secondIndex])+". The color names are: "+str(colors[firstIndex])+"; "+str(colors[secondIndex])+ ". 1 to use part 1, 2 to use part 2. "))
            if choice == 1:
                finalColor = [colorIDs[firstIndex],colors[firstIndex]]
            elif choice == 2:
                finalColor = [colorIDs[firstIndex],colors[firstIndex]]
            else:
                print("failed to select answer")
            #image.close()
        else:
                finalColor = [colorIDs[firstIndex],colors[firstIndex]]
    else:
        finalColor = [colorIDs[0],colors[0]]
    return finalColor
