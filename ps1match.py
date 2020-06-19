import lib.functions as lib
from astropy.table import Table
from time import sleep
import numpy as np
from requests.exceptions import ConnectionError, Timeout, ConnectTimeout
import configparser
import os, sys
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
# 
###################################################################
#verificar se é arquivo sys.argv[1] é um arquivo
data =  Table.read(file).to_pandas()
data.columns = map(str.lower, data.columns)

constraints = {key:value}

fwrite = output
f = open(fwrite,"w+")
# strip blanks and weed out blank and commented-out values
print("Starting....")
f.write(columns.replace("\n"," ") + "\n")
columns = columns.split(',\n')
columns = [x.strip() for x in columns]
columns = [x for x in columns if x and not x.startswith('#')]

length = len(list(data.iterrows()))
array = np.zeros(2*length)
i = 0 
j = 0

for index, row in data.iterrows():
    array[i]= row['ra'] 
    array[i+1] = row['dec']
    i += 2

array = array.reshape(length,2)

if (os.path.exists(sys.argv[2]) == True):
    fopen = open(sys.argv[2],"r")
    j = int(fopen.readline())
    fopen.close()
print(str(j))                        
for line in range(j,length):
    results = None
    while results is None:
        try: 
            ra = array[line][0]
            dec = array[line][1]
            results = lib.ps1cone(ra,dec,radius,release=release,table=table,
                                  columns=columns, verbose=False,**constraints)
            fopen = open(sys.argv[2],"w+")
            fopen.write(str(j))
            fopen.close()
            lines = results.split('\n')
            print(str(j/length*100)," completed")
            f.write('\n'.join(lines[1:]))
            j += 1
        except ConnectionError: 
            print("Connection Error" )
            print("Retrying...")
        except Timeout:
            print("Timeout Error" )
            print("Retrying...")
        except ConnectTimeout:
            print("Timeout Error" )
            print("Retrying...")  
        except ValueError as v:
            print(v)
            print("Some bad cols, exiting..." )
            sys.exit()
        except KeyboardInterrupt:
            sys.exit()
#        except:
#            print("Unknown error..")
#            print("Retrying...")
