import requests
import os
import json
import heapq
import time
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import colorDetect as Color
import PartCategorize as PC
from pathlib import Path
from cameraTesting import camera
from databaseHandler import PartDatabase
from hardwareInterface import hardwareInterfaceHandler as HI

def ask_choice(id1, name1, id2, name2):
    btn1.config(text=f"{id1}: {name1}")
    btn2.config(text=f"{id2}: {name2}")
    choice_var.set(0)
    prompt.grid()                
    root.wait_variable(choice_var)     
    prompt.grid_remove()     
    return choice_var.get()


def idBrick (img):
    with BytesIO() as image_buffer:
        img.save(image_buffer, format="JPEG")
        image_bytes = image_buffer.getvalue()

    res = requests.post(
        'https://api.brickognize.com/predict/?predict_color=true',
        headers={'accept': 'application/json'},
        files={'query_image': ("img.jpg", image_bytes, 'image/jpeg')},
    )

    test = json.loads(res.content)

    
    
    #Lists for possible parts
    partIDs = []
    partNames = []
    partCats = []
    partTypes = []
    partConfidences = []
    
    
    #final part choice, in format [id,name,category,type]
    finalPart = []

    #collect important data about possible parts
    for i in test['items']:
        partIDs.append(i['id'])
        partNames.append(i['name'])
        partTypes.append(i['type'])
        partCats.append(i['category'])
        partConfidences.append(i['score'])
    if len(partIDs)==0:
            return None
    if max(partConfidences) < 0.5:
            return None
    if partTypes[0] != "fig":
        partColor = Color.colorDetection(test)
    else:
        partColor = [None,None]
    #determine if within a percentage, if so, ask which one to use
    if len(partIDs) > 1:
        highestConfidence = max(partConfidences)
        secondHighConf = float(heapq.nlargest(2,partConfidences)[1])
        diff = abs(highestConfidence - secondHighConf) / highestConfidence
        firstIndex = partConfidences.index(highestConfidence)
        secondIndex = partConfidences.index(secondHighConf)

        #if within 20%, show part and ask which one to save
        if diff <= (.10):
            return None
            #image = Image.open(img)
            #image.show()
            #choice = int(input("Part Confidence is within 20% for IDs: "+str(partIDs[firstIndex])+", "+str(partIDs[secondIndex])+". The part names are: "+str(partNames[firstIndex])+"; "+str(partNames[secondIndex])+ ". 1 to use part 1, 2 to use part 2. "))
            choice = ask_choice(partIDs[firstIndex], partNames[firstIndex],
                    partIDs[secondIndex], partNames[secondIndex])
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
    project_dir = Path(__file__).resolve().parent
    p = project_dir / "testImages"
    root = tk.Tk()
    guiImage = tk.Label(root)
    current_label = tk.Label(root, text="-", justify="left")
    log = ScrolledText(root, width=50, height=20)

    guiImage.grid(row=0, column=0, rowspan=2)
    current_label.grid(row=0, column=1)
    log.grid(row=1, column=1)

    choice_var = tk.IntVar(value=0)

    json_files_map = {}
    for config_dir in (
        project_dir,
        project_dir / "sortconfigs",
        project_dir / "subcats",
        project_dir / "subsubcats",
    ):
        if not config_dir.exists():
            continue
        for config_path in config_dir.glob("*.json"):
            with config_path.open("r", encoding="utf-8") as config_file:
                config = json.load(config_file)
            if config.get("sortType", "").strip().lower() not in {
                "colors",
                "categories",
                "subcategories",
                "subsubcategories",
            }:
                continue
            key = str(config_path.relative_to(project_dir))
            json_files_map[key] = str(config_path)

    json_choices = list(json_files_map.keys())

    # Create Combobox for selecting JSON
    json_combobox = ttk.Combobox(
        root, values=json_choices, state="readonly", width=35
    )
    if json_choices:
        json_combobox.set(json_choices[0])
    json_combobox.grid(
        row=2, column=0, columnspan=2, padx=5, pady=5
    )  


    prompt = tk.Frame(root)
    tk.Label(prompt, text="Which part is this?").pack()
    btn1 = tk.Button(prompt, command=lambda: choice_var.set(1))
    btn2 = tk.Button(prompt, command=lambda: choice_var.set(2))
    btn1.pack(fill="x")
    btn2.pack(fill="x")

    prompt.grid(row=3, column=0, columnspan=2, sticky="ew")
    prompt.grid_remove()
    
    cam = camera()
    cam.displayThread.start()
    database = PartDatabase()

    hardwareInter = HI()
    hardwareInter.movementThread.start()
    
    
    run_flag = tk.BooleanVar(value=False)
    tk.Button(root, text="Start", command=lambda: run_flag.set(True)).grid(row=0, column=2, padx=5)
    root.wait_variable(run_flag)
    results = []
    lastResult = None
    result = None
    sampleRateCounter = 0
    while True:

        

        cameraImage = cam.grabImage()
        image = cameraImage
        #img = cameraImage
        #img.thumbnail((400, 400))
        #canvas = Image.new("RGB", (400, 400), "white")
        #canvas.paste(img, ((400 - img.width) // 2, (400 - img.height) // 2))
        #photo = ImageTk.PhotoImage(canvas)
        #guiImage.config(image=photo)
        #guiImage.photo = photo
        #root.update()

        lastResult = result
        
        result = idBrick(image)
        


        #print (result)
        if result != None and lastResult == None:
            time.sleep(0.25)
            cameraImage = cam.grabImage()
            image = cameraImage
            lastResult = result
            result = idBrick(image)
            if result is None:
                continue
            img = cameraImage
            img.thumbnail((400, 400))
            canvas = Image.new("RGB", (400, 400), "white")
            canvas.paste(img, ((400 - img.width) // 2, (400 - img.height) // 2))
            photo = ImageTk.PhotoImage(canvas)
            guiImage.config(image=photo)
            guiImage.photo = photo
            root.update()
            
            selected_key = json_combobox.get()
            selected_json_path = json_files_map[selected_key]

            with open(selected_json_path, "r", encoding="utf-8") as cats:
                binNum = PC.categorize(result, cats)
            
            results.append(result)
            print(result)
            print("")
            hardwareInter.sortBin(binNum)
            database.addPart(result)

            current_label.config(text=f"{result[0]}, {result[4][1]}\n{result[1]}")
            log.insert("end", f"{result[0]}, {result[4][1]}, {result[1]}\n")
            log.see("end")
            root.update()
        time.sleep(0.5)

    root.mainloop()
