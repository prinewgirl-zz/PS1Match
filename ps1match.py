import lib
import sys
from astropy.table import Table
from requests.exceptions import ConnectionError

#verificar se é arquivo sys.argv[1] é um arquivo
data =  Table.read(sys.argv[1]).to_pandas()
data.columns = map(str.lower, data.columns)

radius = 1.0/3600.0
constraints = {'nDetections.gt':1}

fwrite = sys.argv[2]
f = open(fwrite,"w+")
# strip blanks and weed out blank and commented-out values
columns = "objID,raMean,decMean,nDetections,ng,nr,ni,nz,ny," + \
    "gMeanPSFMag,rMeanPSFMag,iMeanPSFMag,zMeanPSFMag,yMeanPSFMag"
    
print("Starting....")
f.write(columns + '\n')
columns = columns.split(',')
columns = [x.strip() for x in columns]
columns = [x for x in columns if x and not x.startswith('#')]                                                 
for index, row in data.iterrows():
    results = None
    while results is None:
        try: 
            ra = row['ra']
            dec = row['dec']
            results = lib.ps1cone(ra,dec,radius,release='dr2',columns=columns,
                                  verbose=False,**constraints)
            lines = results.split('\n')
            print(len(lines),"rows in results -- first 5 rows:")
            print('\n'.join(lines[1:6]))  
            f.write('\n'.join(lines[1:]))
        except ConnectionError: 
            print("Connection Error" )
            print("Retrying...")
                
