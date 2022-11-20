# check if number is prime
import os
import requests

print('main.py')
datadir = 'nyc-taxi-tiny'
os.makedirs( datadir, exist_ok=True)

manifest_fname = 'fileurls.txt'

bucket = "https://voltrondata-labs-datasets.s3.us-east-2.amazonaws.com"
pagesroot = 'https://jzavala-gonzalez.github.io/nyc-taxi-tiny/'

years = list(range(2009,2023))
months = list(range(1,13))

urls = []
for y in years:
    for m in months:
        dpath = os.path.join('nyc-taxi-tiny', f'year={y}', f'month={m}')
        # print(dpath)
        os.makedirs(dpath, exist_ok=True)
        durl = os.path.join(bucket, dpath, "part-0.parquet")
        purl = os.path.join(pagesroot, dpath, 'part-0.parquet')
        #print(durl)
        dfile = os.path.join(dpath, 'part-0.parquet')
        if os.path.exists(dfile):
            urls.append(purl)
            continue

        r = requests.get(durl)
        if r.status_code != 200:
            print(durl, r.status_code)
            continue

        
        with open(dfile, 'wb') as f:
                f.write(r.content)

        urls.append(purl)

    break



with open(manifest_fname, 'w') as f:
    f.write('\n'.join(urls))


# from dataset_check import *