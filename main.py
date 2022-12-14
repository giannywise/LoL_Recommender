import sys
import os
try:
    del sys.modules['extraction']
except KeyError:
    pass
import extraction as ex


"""

Datenvextraktions Struktur

Summoner Name --> summoner puuid --> matchhistory by puuid --> mathes by id --> grouped by champions

commands to upload to docker:

docker build --platform linux/amd64 -t lol-rmv2 .  --> build image for apple sillicon
docker tag lol-rmv2:latest giannywise/test:lol-rmv2
docker push giannywise/test:lol-rmv2

commands to run image on server:

docker pull giannywise/test:lol-rmv2
docker run -it giannywise/test:lol-rmv2

kopieren von Dateien in Containern: docker cp <containerID>:<datei> /Desktop


"""
try:
    os.mkdir('matches')
    print('Folder created')
except FileExistsError:
    pass

ex.get_match_info()
