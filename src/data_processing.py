import os
import random
import pandas as pd

# Data storage folder
folder_path = "data/"

# Selects a random CSV file from the data folder
def randomData(folder_path):
    csvFiles = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            csvFiles.append(filename)
    selectedFile = random.choice(csvFiles)
    return os.path.join(folder_path, selectedFile)


# Loads the data from the randomly selected CSV file
# Removes unnecessary rows and renames columns
# Converts time to EST
def loadData(filepath):
    rawData = pd.read_csv(filepath, skiprows = 3, header = None)
    rawData.columns = ["Datetime", "Close", "High", "Low", "Open", "Volume"]
    data = rawData[["Datetime", "Close", "High", "Low", "Open", "Volume"]]
    data["Datetime"] = pd.to_datetime(data["Datetime"], utc = True)
    data["Datetime"] = data["Datetime"].dt.tz_localize(None) - pd.Timedelta(hours=4)
    data["Time"] = data["Datetime"].dt.strftime("%H:%M:%S")
    data["Timestamp"] = data["Datetime"]
    
    data = data.drop(columns=["Datetime"])
    return data


# Testing purposes (DO NOT EDIT)
def main():
    # Select random CSV file
    randomCSV = randomData(folder_path)
    print(f"Randomly selected CSV: {randomCSV}")

    # Load the data
    rawData = loadData(randomCSV)
    print("Raw Data: ")
    print(rawData.head())

# Boilerplate
if __name__ == "__main__":
    main()
