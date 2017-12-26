# athor: Rodd Talebi
# objective: combine similar .xlsx files


import pandas as pd
import os
import glob

PATHNAME = raw_input("\nWhat is the path name of the folder the .csv files are located in?\nNote this will combine all .csv files in the folder.\n")
NEWFILENAME = raw_input("\nAnd what would you like to name the new file?\n[ADD THE .XLSX EXTENSION YOURSELF PLS]\n")

os.chdir(PATHNAME)
FILENAMES = glob.glob("*.csv")
FILENAMES = [file for file in FILENAMES if "$" not in file]
print "\nWe will combine the following files:\n", FILENAMES, "\n", "\nand save them to:\n", NEWFILENAME

print "\nrunning..."
all_data = pd.DataFrame()
for f in FILENAMES:
    df = pd.read_csv(f)
    df["Source File"] = f
    all_data = all_data.append(df, ignore_index=True)

#writer = pd.ExcelWriter(NEWFILENAME, engine='xlsxwriter')
#all_data.to_excel(writer, sheet_name='Sheet1')
all_data.to_csv(NEWFILENAME)
#writer.save()


print "\nDONE AND SAVED"