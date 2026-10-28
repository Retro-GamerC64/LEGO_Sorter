import requests
import os
import json
import heapq
import time
from pathlib import Path
from PIL import Image
import colorDetect as Color

def idBrick (img):
    res = requests.post(
        'https://api.brickognize.com/predict/?predict_color=true',
        headers={'accept': 'application/json'},
        files={'query_image': ("img.jpg", img, 'image/jpeg')},
    )

    test = json.loads(res.content)

    #Lists for possible parts
    partIDs = []
    partNames = []
    partCats = []
    partTypes = []
    partConfidences = []
    partColor = Color.colorDetection(test)
    #final part choice, in format [id,name,category,type]
    finalPart = []

    #collect important data about possible parts
    for i in test['items']:
        partIDs.append(i['id'])
        partNames.append(i['name'])
        partTypes.append(i['type'])
        partCats.append(i['category'])
        partConfidences.append(i['score'])

    #determine if within a percentage, if so, ask which one to use
    if len(partIDs) > 1:
        highestConfidence = max(partConfidences)
        secondHighConf = float(heapq.nlargest(2,partConfidences)[1])
        diff = abs(highestConfidence - secondHighConf) / highestConfidence
        firstIndex = partConfidences.index(highestConfidence)
        secondIndex = partConfidences.index(secondHighConf)

        #if within 20%, show part and ask which one to save
        if diff <= (.20):
            image = Image.open(img)
            image.show()
            choice = int(input("Part Confidence is within 20% for IDs: "+str(partIDs[firstIndex])+", "+str(partIDs[secondIndex])+". The part names are: "+str(partNames[firstIndex])+"; "+str(partNames[secondIndex])+ ". 1 to use part 1, 2 to use part 2. "))
            if choice == 1:
                finalPart = [partIDs[firstIndex],partNames[firstIndex],partTypes[firstIndex],partCats[firstIndex],partColor]
            elif choice == 2:
                finalPart = [partIDs[secondIndex],partNames[secondIndex],partTypes[secondIndex],partCats[secondIndex],partColor]
            else:
                print("failed to select answer")
            image.close()
        else:
                finalPart = [partIDs[firstIndex],partNames[firstIndex],partTypes[firstIndex],partCats[firstIndex],partColor]
    else:
        finalPart = [partIDs[0],partNames[0],partTypes[0],partCats[0],partColor]

    #return the final choice
    return finalPart




if __name__ == "__main__":
    images = []
    results = []
    p = Path(__file__).resolve().parent / "testImages"

    for e in os.scandir(p):
        if e.is_file():
            image = open(e.path,'rb')
            images.append(image)
    for imag in images:
        result = idBrick(imag)
        print(result)
        results.append(result)
        time.sleep(0.5)
        
    print(results)





