import requests
import os
import json
import heapq
import time

def categorize(partData, cats):
    partID = partData[0]
    partName = partData[1]
    partType = partData[2]
    partCat = partData[3]
    if isinstance(partCat, (list, tuple)):
        partCategories = [str(category).strip().lower() for category in partCat if category]
    else:
        partCategories = [str(partCat).strip().lower()]
    if partType != "fig":
        partColor = partData[4][1]
        partColorID = partData[4][0]
        categories = json.load(cats)
        categoryOverride = categories.get("categoryOverrides", {}).get(
            str(partID).strip().lower()
        )
        if categories["sortType"] == "subcategories" and categoryOverride:
            partCategories = [str(categoryOverride).strip().lower()]
        binNames = [
            name for name in categories if name not in {"sortType", "categoryOverrides"}
        ]
        binNum = 0

        if categories["sortType"] == "colors":
            if partColorID is None:
                print("No color prediction available; cannot route to a color bin.")
                return None
            for i in binNames:
                itemIndex = binNum
                for j in categories[i]:
                    if int(j) == int(partColorID):
                        print("Color: "+ str(i)+", ID#: "+str(j))
                        return itemIndex
                binNum = binNum+1

        elif categories["sortType"] == "categories":
            for partCategory in partCategories:
                for i in binNames:
                    itemIndex = binNum
                    for j in categories[i]:
                        if str(j).strip().lower() == partCategory:
                            print("Category: " + str(partCat) + ", Top Level Category: " + i)
                            return itemIndex
                    binNum = binNum + 1
                binNum = 0
        elif categories["sortType"] == "subcategories":
            for partCategory in partCategories:
                for i in binNames:
                    itemIndex = binNum
                    for j in categories[i]:
                        if str(j).strip().lower() == partCategory:
                            print("Category: " + str(partCat) + ", Subcategory: " + i)
                            return itemIndex
                    binNum = binNum + 1
                binNum = 0
        elif categories["sortType"] == "subSubcategories":
            for i in binNames:
                itemIndex = binNum
                for j in categories[i]:
                    if str(j).strip().lower() == str(partID).strip().lower():
                        print("Subcategory: " + str(partCat) + ", Sub-Subcategory: " + i)
                        return itemIndex
                binNum = binNum + 1
        