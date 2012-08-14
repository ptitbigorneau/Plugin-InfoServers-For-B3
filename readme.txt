# infoservers plugin
# Plugin for B3 (www.bigbrotherbot.com)
# www.ptitbigorneau.fr

need qstat (http://sourceforge.net/projects/qstat/files/qstat/)

infoservers plugin (v1.2.2) for B3

Installation:

1. Place the infoservers.py in your ../b3/extplugins and the 
infoservers.xml in your ../b3/extplugins/conf folders.

2. Open infoservers.xml

modify command qstat

for linux                <set name="commandqstat">qstat</set>
or for debian / ubuntu   <set name="commandqstat">quakestat</set>
for windows (the path of the executable qstat.exe) exemple <set name="commandqstat">C:\qstat-2.11-win32\qstat.exe</set>

3. Open your B3.xml file (default in b3/conf) and add the next line in the
<plugins> section of the file:

<plugin name="infoservers" config="@b3/extplugins/conf/infoservers.xml"/>

4. Run the infoservers SQL script on your B3 database

5. add servers with command !addservers or !aserv <game,adress,gametype>

exemple 
!addservers Urban Terror,95.130.9.86:27960,-q3s
!addservers Smokin Guns,95.130.9.86:27960,-q3s

gametype :

-q3s for quake3 games (urban terror, tremulous, smokin guns, World of Padman ...)
-cods for call of duty games
-woets for Enemy Territory games
-a2s for hl2 games
...
see qstat gametype.txt