import lib
from astropy.table import Table
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
for index, row in data.iterrows():
    results = None
    while results is None:
        try: 
            ra = row['ra']
            dec = row['dec']
            results = lib.ps1cone(ra,dec,radius,release=release,table=table,
                                  columns=columns, verbose=False,**constraints)
            lines = results.split('\n')
            print(len(lines)-1,"rows in results -- first 5 rows:")
            #print('\n'.join(lines[1:6]))  
            f.write('\n'.join(lines[1:]))
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
        except:
            print("Unknown error..")
            print("Retrying...")
