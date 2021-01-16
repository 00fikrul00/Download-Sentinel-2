from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import os,sys
print(sys.version)
import subprocess
from glob import glob
import csv
import zipfile
import datetime
from datetime import datetime, timedelta
import pandas
from collections import OrderedDict
import collections
import time
from time import sleep

waktu_awal = raw_input("Enter waktu mulai - Exp(yyyymmdd): ")
str_waktuawal = str(waktu_awal)
waktu_akhir = str(raw_input("Enter waktu akhir - Exp(yyyymmdd): "))

a = datetime.strptime(waktu_awal, '%Y%m%d')
b = datetime.strptime(waktu_akhir, '%Y%m%d') 
delta = b - a
jumlah = int(delta.days) + 1

path = 'D:/GET_SENTINEL'
ingeojson = glob(os.path.join(path + '/' +'**.geojson'))
print ingeojson[0]

for i in range(jumlah):
    try:
        jj = a + timedelta(days=i)
        dtlist = str(jj.strftime("%Y%m%d"))
        yylist = int(jj.strftime("%Y"))
        mmlist = int(jj.strftime("%m"))
        ddlist = int(jj.strftime("%d"))+1
        print dtlist, yylist, mmlist, ddlist

        api = SentinelAPI('fikrul02', 'zse123mko123',
                          'https://scihub.copernicus.eu/dhus',
                          show_progressbars=True)

        # search by polygon, time, and Hub query keywords
        footprint = geojson_to_wkt(read_geojson(ingeojson[0]))

        products = api.query(footprint,
                            date= (dtlist, date(yylist, mmlist, ddlist)),
                            platformname='Sentinel-2',
                            cloudcoverpercentage=(0, 15),
                            producttype = 'S2MSI1C')
        getid = collections.OrderedDict(sorted(products.items(), key=lambda x:x[1]))
        key_getid = getid.keys()
        product_info = api.get_product_odata(str(key_getid[0]))
        print str(product_info['title'])
        
        #download all results from the search
        api.download_all(products, directory_path='D:/GET_SENTINEL/DOWNLOAD', checksum=True)
        with click.progressbar(length=total_size, label='Downloading files') as bar:
            for file in api.download_all(products, directory_path='D:/GET_SENTINEL/DOWNLOAD', checksum=True):
                download(file)
                bar.update(file.size)
    except Exception:
        pass
        
