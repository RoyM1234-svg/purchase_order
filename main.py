import csv
import pandas as pd
import numpy as np
import os
import sys



def split_tables(df,count = 0):
    df_pirzool = pd.DataFrame(columns = ["ITEM","AMOUNT","TOTAL PRICE"])
    df_konstrok = pd.DataFrame(columns = ["ITEM","LEN","AMOUNT","SUM LEN","KG/PER","TOTAL KG","TOTAL PRICE"]) 
    for index in df.index:
        count += 1
        if df.loc[index,"ITEM"] == 'פרזול':
            for i in df.index[count:]:
                amount = df.loc[i,"AMOUNT"]
                price = df.loc[i,"SUM LEN"]
                df_pirzool.loc[i,"AMOUNT"] = amount
                df_pirzool.loc[i,"TOTAL PRICE"] = price
                df_pirzool.loc[i,"ITEM"] = df.loc[i,"ITEM"]
            return df_konstrok, df_pirzool
        data = df.loc[index]
        df_konstrok = df_konstrok.append(data,ignore_index = True)
        
    return ("wrong format")

def clean_table(df,name):
    df.dropna(how = 'all', inplace = True,subset = df.columns[1:])

    
def fill_konstrok(df_konstrok,name):
    df_konstrok['SUM LEN'] = df_konstrok['LEN'] * df_konstrok['AMOUNT']
    df_konstrok['NAME'] = name
    df_konstrok.loc[df_konstrok['ITEM'].str.contains('זווית'),'TOTAL KG'] = df_konstrok['SUM LEN'] * 0.623
    df_konstrok.loc[df_konstrok['ITEM'].str.contains('קושרת'),'TOTAL KG'] = df_konstrok['SUM LEN'] * 1.03

def fill_pirzool(df_pirzool,name):
    df_pirzool['NAME'] = name

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: unvalid data")
    else:
        filename = sys.argv[1]
        midname = filename.split("/")[-1]
        name = midname.split(".")[0]

     
    df = pd.read_csv(filename ,names = ["ITEM","LEN","AMOUNT","SUM LEN","KG/PER","TOTAL KG","TOTAL PRICE"])
    df = df.dropna(how ='all',subset=['ITEM'])
    df[["LEN", "AMOUNT"]] = df[["LEN", "AMOUNT"]].apply(pd.to_numeric)
    # לוקח את הקובץ ומפרק אותו לטבלה של קונסטרוקציה וטבלה של חומר פרזול
    df_konstrok, df_pirzool = split_tables(df)
    # מפרק את הטבלה של הקונסטרוציה לטבלה של דיאגונלים ואגדים ולטבלה של קושרות
    clean_table(df_konstrok,name)
    clean_table(df_pirzool,name)
    fill_konstrok(df_konstrok,name)
    fill_pirzool(df_pirzool,name)

    # final_df = df_konstrok.groupby(['NAME','ITEM']).sum()
    # final_df = pd.pivot_table(df_konstrok, index = ['NAME'], columns = ['ITEM'],values = ['SUM LEN','TOTAL KG'], aggfunc = np.sum)
    # print(final_df)
    
  

    

    konstrok_file = "konstrok.csv"
    pirzool_file = "pirzool.csv"
    # diag_file = "diag.csv"
    # pivot_file = "pivot.csv"
    df_konstrok.to_csv(konstrok_file, index=False, header = False)
    df_pirzool.to_csv(pirzool_file, index = False, header = False)
    # df_diag.to_csv(diag_file, index = False)
    # final_df.to_csv(pivot_file)

    

if __name__ == "__main__":
    main()