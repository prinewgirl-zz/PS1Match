import lib
from astropy.table import Table
from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout
from urllib3.exceptions import ReadTimeoutError
import os
import configparser
config = configparser.ConfigParser()

###################################################################
# Import configparser
###################################################################

config.read(os.path.join(os.getcwd(),"parameters.ini"))

file                      = config.get(       "General","file")
output                    = config.get(       "General","output")
release                   = config.get(       "Query","release")
table                     = config.get(       "Query","table")
columns                   = config.get(       "Query","columns")
radius                    = config.get(       "Query","radius")
key                       = config.get(       "Query","key")
value                     = config.get(       "Query","value")

###################################################################
# Import configparser
###################################################################

#verificar se é arquivo sys.argv[1] é um arquivo
data =  Table.read(file).to_pandas()
data.columns = map(str.lower, data.columns)

#radius = 1.0/3600.0
constraints = {key:value}

fwrite = output
f = open(fwrite,"w+")
# strip blanks and weed out blank and commented-out values
#columns = "objID,raMean,decMean,nDetections,ng,nr,ni,nz,ny," + \
#    "gMeanPSFMag,rMeanPSFMag,iMeanPSFMag,zMeanPSFMag,yMeanPSFMag"
    
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
            results = lib.ps1cone(ra,dec,radius,release=release,columns=columns,
                                  verbose=False,**constraints)
            lines = results.split('\n')
            print(len(lines),"rows in results -- first 5 rows:")
            print('\n'.join(lines[1:6]))  
            f.write('\n'.join(lines[1:]))
        except ConnectionError: 
            print("Connection Error" )
            print("Retrying...")
        except ReadTimeout:
            print("Read Timeout")
            print("Retrying...")
        except  ReadTimeoutError:
            print("Read Timeout")
            print("Retrying...")
f.close()