import lib
import sys
from astropy.table import Table
#verificar se é arquivo sys.argv[1] é um arquivo
data =  Table.read(sys.argv[1]).to_pandas()
data.columns = map(str.lower, data.columns)

radius = 1.0/3600.0
constraints = {'nDetections.gt':1}

# strip blanks and weed out blank and commented-out values
columns = """objID,raMean,decMean,nDetections,ng,nr,ni,nz,ny,
    gMeanPSFMag,rMeanPSFMag,iMeanPSFMag,zMeanPSFMag,yMeanPSFMag""".split(',')
columns = [x.strip() for x in columns]
columns = [x for x in columns if x and not x.startswith('#')]

for i in range(len(data)):
    ra = data.loc(i,"ra")
    dec = data.loc(i,"dec")
    results = lib.ps1cone(ra,dec,radius,release='dr2',columns=columns, verbose=True,**constraints)
    lines = results.split('\n')
    print(len(lines),"rows in results -- first 5 rows:")
    print('\n'.join(lines[:6]))

    