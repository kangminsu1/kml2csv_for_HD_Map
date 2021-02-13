# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import csv
from re import sub
import sys
import os

def populate_data(kml,writer):
    for pm in kml.find_all('Placemark'):
        data = []
        coords = pm.contents[9].coordinates.string
        coords = sub(r'(\n|\s)+','',coords).split(',')

        if len(coords) <= 3:
            data.append(coords[1]) # lat
            data.append(coords[0]) # long
            data.append(coords[2])
            for i in range(len(data)):
                if data[i-1] is None:
                    del data[i-1]
            writer.writerow(data)
        else:
            for i in range(len(coords)):
                if i % 2 == 0:
                    data = []
                    r = coords[i].split('.')
                    try:
                        if not r[2] == None:
                            tt = int(r[1]) % 1000
                            height = int(r[0]) + float(r[1]) / pow(10, len(r[1]))
                            longitude = tt + float(r[2]) / pow(10, len(r[2]))
                            latitude = coords[i+1]
                            data.append(latitude)
                            data.append(longitude)
                            data.append(height)
                            writer.writerow(data)
                    except:
                        pass

def main(inputfile,outputfile):
    with open(inputfile, 'r',  encoding='UTF8') as f:
        kml = BeautifulSoup(f, 'xml')
        with open(outputfile, 'w', encoding='UTF8') as csvfile:
            print(outputfile + " processing..")
            writer = csv.writer(csvfile)
            populate_data(kml,writer)
        print(outputfile + " clear!")

if __name__ == "__main__":
    print("****************Build from Kang Min Su***************")
    print("This is convert .kml to .csv file [DATA: LLH]")
    print("Converting START")

    location = './'
    directory = os.listdir(location)
    count = 0
    for name in directory:
        r = name.split('.')
        if not r[1] == 'kml':
            del directory[count]
        count += 1
    print("Finded FILES:",directory)

    for name in directory:
        r = name.split('.')
        inputfile = name
        outputfile = r[0] + '.csv'
        main(inputfile, outputfile)

