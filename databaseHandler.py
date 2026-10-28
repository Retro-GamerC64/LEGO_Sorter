import sqlite3
from datetime import datetime
class PartDatabase:
    def __init__(self):
        self.catalog = sqlite3.connect('catalog.db')
        logTime = datetime.now()
        self.logTitle = logTime.strftime("%m_%d_%Y___%H_%M_%S")
        print(self.logTitle)
        self.catalog.execute(f"""CREATE TABLE "{self.logTitle}"(
        row INTEGER PRIMARY KEY AUTOINCREMENT,
        id       INTEGER,
        name     TEXT NOT NULL,
        type     TEXT,
        category TEXT,
        color_name INTEGER,
        color_id TEXT
        );""")
        self.catalog.commit()           

    def addPart(self, part):
        partID = part[0]
        partName = part[1]
        partType = part[2]
        partCat = part[3]
        partColor = part[4][1]
        partColorID = part[4][0]
        for i, val in enumerate(part):
            if val is list:
                for j, jval in enumerate(i):
                    if jval == None:
                        part[i][j] = 'None'
            else:
                if val == None:
                    part[i] = "None"
        query = f"""INSERT INTO "{self.logTitle}" 
                    (id, name, type, category, color_id, color_name) 
                    VALUES (?, ?, ?, ?, ?, ?)"""
        self.catalog.execute(query, (partID, partName, partType, partCat, partColorID, partColor))
        self.catalog.commit()
