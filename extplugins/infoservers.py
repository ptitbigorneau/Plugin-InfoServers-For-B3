# InfoServers Plugin

__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '1.2.2'


import b3, threading, thread, time
import b3.plugin
import os 

class InfoserversPlugin(b3.plugin.Plugin):

    _adminPlugin = None
    
    def onStartup(self):
        
        self._adminPlugin = self.console.getPlugin('admin')
        
        if not self._adminPlugin:

            self.error('Could not find admin plugin')
            return False
    
        self._adminPlugin.registerCommand(self, 'infoservers',self._userserverslevel, self.cmd_infoservers, 'iserv')
        self._adminPlugin.registerCommand(self, 'addservers',self._admserverslevel, self.cmd_addservers, 'aserv')
        self._adminPlugin.registerCommand(self, 'delservers',self._admserverslevel, self.cmd_delservers, 'dserv')
        self._adminPlugin.registerCommand(self, 'listservers',self._userserverslevel, self.cmd_listservers, 'lserv')
        self._adminPlugin.registerCommand(self, 'listplayersserver',self._userserverslevel, self.cmd_listplayersserver, 'lpserv')
        self._adminPlugin.registerCommand(self, 'whereplayers',self._userserverslevel, self.cmd_whereplayers, 'wplayers')
    
    def onLoadConfig(self):
    
        self._userserverslevel = self.config.getint('settings', 'userserverslevel')
        self._admserverslevel = self.config.getint('settings', 'admserverslevel')
        self._commandqstat = self.config.get('settings', 'commandqstat')

    def cmd_infoservers(self, data, client, cmd=None):
        
        """\
        Info other game servers
        """
        
        if not data.isdigit():
        
            client.message('!infoservers <server id>')
            
            return
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            
            client.message('!infoservers <server id>')
            
            return
            
        id=input[0]
        
        thread.start_new_thread(self.infoservers, (data, client, id))
            
    def infoservers(self, data, client, id):        
        
        cursor = self.console.storage.query("""
        SELECT *
        FROM server
        WHERE id = %s
        """ % (id))
        
        if cursor.rowcount == 0:
          
            client.message("^7This server id (^1%s^7) does not exist"%(id))
            cursor.close()            
            
            return False
        
        else:
            
            sr = cursor.getRow()
            
            cgame = sr['game']
            cadress = sr['adress']
            cgametype = sr['gametype']
            
            command=os.popen(self._commandqstat + " -xml " + str(cgametype) + " " + str(cadress))
            resultat=command.read()
            command.close()

            resultat = resultat.split('\n')
                 
            if ('DOWN' in resultat[2]) or ('TIMEOUT' in resultat[2]):

                client.message('^3-------------------Server-------------------')
                client.message('^3Server Id : ^5%s^3'%(id))
                client.message('^3Server : ^1Offline')
                client.message('^3Adress : ^5%s^3'%(adresse))
                client.message('^3--------------------------------------------')
    
            if 'UP' in resultat[2]:

                name= resultat[4].replace('<name>', '')
                name= name.replace('</name>', '')
                name= name.replace('    ', '')
    
                adresse= resultat[3].replace('<hostname>', '')
                adresse= adresse.replace('</hostname>', '')
                adresse= adresse.replace('    ', '')
    
                map= resultat[6].replace('<map>', '')
                map= map.replace('</map>', '')
                map= map.replace('    ', '')
                
                nplayer= resultat[7].replace('<numplayers>', '')
                nplayer= nplayer.replace('</numplayers>', '')
                nplayer= nplayer.replace('    ', '')

                slots= resultat[8].replace('<maxplayers>', '')
                slots= slots.replace('</maxplayers>', '')
                slots= slots.replace('    ', '')
            
                client.message('^3-------------------Server-------------------')
                client.message('^3Server Id : ^5%s^3'%(id))
                client.message('^3Name : ^5%s^3'%(name))
                client.message('^3Game : ^5%s^3'%(cgame))
                client.message('^3Server : ^2Online')
                client.message('^3Adress : ^5%s^3'%(adresse))
                client.message('^3Map : ^5%s^3'%(map))
                client.message('^3Player(s)/Slots : ^5%s^3/^5%s^3'%(nplayer, slots))
                client.message('^3--------------------------------------------')
            
            cursor.close()
            
    def cmd_addservers(self, data, client, cmd=None):
    
        """\
        Add server <game,adress server,typegame>
        """

        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            
            client.message('!addservers <game,adress server,typegame>')
            
            return
        
        if input[1]:
        
            tdata=input[0]+input[1]
        
        else:
        
            tdata=input[0]
        
        nvirg= tdata.count(',')
        
        if (nvirg==0) and (nvirg>3):
            
            client.message('!addservers <game,adress server,typegame>')
            
            return False        
        
        tdata = tdata.split(',')
        game = tdata[0]
        adress = tdata[1]
        gametype = tdata[2]            
        
        if adress.count(':') == 0:
        
            client.message('Bad adress server !')
            
            return False    

        if adress.count('.') != 3:
        
            client.message('Bad adress server !')
            client.message('exemple adress server : 95.130.9.86:27960')

            return False

        if gametype.count('-') != 1:
        
            client.message('Bad gametype !')
            client.message('gametype : -q3s or -a2s or -cods or -woets...')

            return False            
        
        command=os.popen(self._commandqstat + " -xml " + str(gametype) + " " + str(adress))
        resultat=command.read()
        command.close()

        if resultat == '':
        
            client.message('Bad gametype !')
            client.message('gametype : -q3s or -a2s or -cods or -woets ...')

            return False
        
        if game:
            
            cursor = self.console.storage.query("""
            SELECT *
            FROM server n 
            WHERE n.adress = '%s'
            """ % (adress))

            if cursor.rowcount > 0:
                
                cursor = self.console.storage.query("""
                UPDATE server
                SET game='%s', gametype='%s' 
                WHERE adress = '%s'
                """ % (game, gametype, adress))
                client.message('This new game server is now registered')
                cursor.close()
                
                return False
            
            cursor.close()
            
            cursor = self.console.storage.query("""
            SELECT *
            FROM server
            ORDER BY id
            """)
            
            tid = 1
            
            if cursor.EOF:
          
                tid = 1

            while not cursor.EOF:
            
                sr = cursor.getRow()
                id = sr['id']
                
                if tid == id:
    
                    tid += 1
                     
                else:
    
                    tid = tid
                          
                cursor.moveNext()
            
            
            cursor = self.console.storage.query("""
            INSERT INTO server
            VALUES ('%s', '%s', '%s', '%s')
            """ % (tid, game, adress, gametype))
            
            cursor.close()
            client.message('This game server is now registered')
       
        else:
            return False
            
    def cmd_delservers(self, data, client, cmd=None):
        """\
        Delete server <server id>
        """

        if not data.isdigit():
        
            client.message('!delservers <server id>')
            
            return        
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            
            client.message('!delservers <server id>')
            
            return
            
        id=input[0]
        
        if (id < 1) and (id > 99):
        
            client.message('!delservers <server id>')
            
            return

        cursor = self.console.storage.query("""
        SELECT id
        FROM server
        WHERE id = %s
        """ % (id))
        
        if cursor.rowcount == 0:
            
            client.message("^7This server id (^1%s^7) does not exist"%(id))
            
            return False
        
        cursor.close()
        
        cursor = self.console.storage.query("""
        DELETE FROM server
        WHERE id = '%s'
        """ % (id))
        cursor.close()
        
        client.message("^7Server has been deleted")
    
    def cmd_listservers(self, data, client, cmd=None):
        
        """\
        Servers list 
        """
        
        thread.start_new_thread(self.listservers, (data, client))
        
    def listservers(self, data, client):
            
        cursor = self.console.storage.query("""
        SELECT *
        FROM server
        ORDER BY id
        """)
        
        c = 1
        
        if cursor.EOF:
          
            client.message('Servers list is empty')
            cursor.close()            
            
            return False
        
        while not cursor.EOF:
            
            sr = cursor.getRow()
            cid = sr['id']
            cgame = sr['game']
            cadress = sr['adress']
            cgametype = sr['gametype']
            
            command=os.popen(self._commandqstat + " -xml " + str(cgametype) + " " + str(cadress))
            resultat=command.read()
            command.close()

            resultat = resultat.split('\n')
                    
                
            if ('DOWN' in resultat[2]) or ('TIMEOUT' in resultat[2]):


                client.message('^3ID : ^5%s^3 - Server : ^5%s^1 Down^3'%(str(cid), cadress))

                
                cursor.moveNext()
    
            if 'UP' in resultat[2]:

                name= resultat[4].replace('<name>', '')
                name= name.replace('</name>', '')
                name= name.replace('&amp;', '&')
                name= name.replace('    ', '')
    

                client.message('^3ID : ^5%s^3 - Server : ^5%s^3'%(str(cid), name))

                 
                cursor.moveNext()
            
            c += 1
            
        cursor.close()
        
    def cmd_listplayersserver(self, data, client, cmd=None):
        
        """\
        Info other game servers
        """
        
        if not data.isdigit():
        
            client.message('!listplayersserver <server id>')
            
            return        
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            
            client.message('!listplayersserver <server id>')
            
            return
            
        id=input[0]
        
        if (id < 1) and (id > 99):
        
            client.message('!listplayersserver <server id>')
            
            return
            
        thread.start_new_thread(self.listplayersserver, (data, client, id))
            
    def listplayersserver(self, data, client, id):        
        
        cursor = self.console.storage.query("""
        SELECT *
        FROM server
        WHERE id = %s
        """ % (id))
        
        if cursor.rowcount == 0:
          
            client.message("^7This server id (^1%s^7) does not exist"%(id))
            cursor.close()            
            
            return False
        
        else:
            
            sr = cursor.getRow()
            
            cgame = sr['game']
            cadress = sr['adress']
            cgametype = sr['gametype']
            
            command=os.popen(self._commandqstat + " -xml " + str(cgametype) + " " + str(cadress))
            resultat=command.read()
            command.close()

            resultat = resultat.split('\n')
                 
            if ('DOWN' in resultat[2]) or ('TIMEOUT' in resultat[2]):

                client.message('^3-------------------Server-------------------')
                client.message('^3Server Id : ^5%s^3'%(id))
                client.message('^3Server : ^1Offline')
                client.message('^3Adress : ^5%s^3'%(adresse))
                client.message('^3--------------------------------------------')

                cursor.moveNext()
    
            if 'UP' in resultat[2]:

                name= resultat[4].replace('<name>', '')
                name= name.replace('</name>', '')
                name= name.replace('&amp;', '&')
                name= name.replace('    ', '')
    
                adresse= resultat[3].replace('<hostname>', '')
                adresse= adresse.replace('</hostname>', '')
                adresse= adresse.replace('    ', '')
    
                map= resultat[6].replace('<map>', '')
                map= map.replace('</map>', '')
                map= map.replace('    ', '')
                
                nplayer= resultat[7].replace('<numplayers>', '')
                nplayer= nplayer.replace('</numplayers>', '')
                nplayer= nplayer.replace('    ', '')

                slots= resultat[8].replace('<maxplayers>', '')
                slots= slots.replace('</maxplayers>', '')
                slots= slots.replace('    ', '')
            
            if nplayer == '0':
                
                client.message('^3-------------------Server-------------------')
                client.message('^3Server Id : ^5%s^3'%(id))
                client.message('^3Name : ^5%s^3'%(name))
                client.message('^3No player on the server : ^1%s^3/^5%s^3'%(nplayer, slots))
                client.message('^3--------------------------------------------')
                
            else:
            
                client.message('^3-------------------Server-------------------')
                client.message('^3Server Id : ^5%s^3'%(id))
                client.message('^3Name : ^5%s^3'%(name))
                client.message('^3Player(s) on the server : ^1%s^3/^5%s^3'%(nplayer, slots))
                client.message('^3-------------------Player-------------------')

                command=os.popen(self._commandqstat + " -P " + str(cgametype) + " " + str(cadress))
                resultat=command.read()
                command.close()

                resultat = resultat.split('\n')
                
                for ligne in resultat:
                    
                    if 'frags' in ligne:
                                            
                        ligne = ligne.replace('\t', '')
                        ligne = ligne.replace('  ', ' ')
                        ligne = ligne.split(' ')
                        
                        if ligne[0] != '':
                        
                            if ligne[3] != '':
                        
                                pname = ligne[4]
                                pscore = ligne[0]
                                pping = ligne[3].replace('ms', '')

                            if ligne[3] == '':
                        
                                pname = ligne[5]
                                pscore = ligne[0]
                                pping = ligne[4].replace('ms', '')
                            
                        if ligne[0] == '':
                        
                            if ligne[4] != '':
                        
                                pname = ligne[5]
                                pscore = ligne[1]
                                pping = ligne[4].replace('ms', '')

                            if ligne[4] == '':
                        
                                pname = ligne[6]
                                pscore = ligne[1]
                                pping = ligne[5].replace('ms', '')

                        client.message('^5%s^3 - Score : ^5%s^3 - Ping : ^5%s^7'%(pname, pscore, pping))
                        
    def cmd_whereplayers(self, data, client, cmd=None):
        
        """\
        On what servers there any players?
        """
        
        thread.start_new_thread(self.whereplayers, (data, client))
        
    def whereplayers(self, data, client):
            
        cursor = self.console.storage.query("""
        SELECT *
        FROM server
        ORDER BY id
        """)
        
        c = 1
        
        if cursor.EOF:
          
            client.message('Servers list is empty')
            cursor.close()            
            
            return False
        
        while not cursor.EOF:
            
            sr = cursor.getRow()
            cid = sr['id']
            cgame = sr['game']
            cadress = sr['adress']
            cgametype = sr['gametype']
            
            command=os.popen(self._commandqstat + " -xml " + str(cgametype) + " " + str(cadress))
            resultat=command.read()
            command.close()

            resultat = resultat.split('\n')
                    
                
            if ('DOWN' in resultat[2]) or ('TIMEOUT' in resultat[2]):

                cursor.moveNext()
    
            if 'UP' in resultat[2]:

                name= resultat[4].replace('<name>', '')
                name= name.replace('</name>', '')
                name= name.replace('    ', '')
                name= name.replace('&amp;', '&')
                
                nplayer= resultat[7].replace('<numplayers>', '')
                nplayer= nplayer.replace('</numplayers>', '')
                nplayer= nplayer.replace('    ', '')

                slots= resultat[8].replace('<maxplayers>', '')
                slots= slots.replace('</maxplayers>', '')
                slots= slots.replace('    ', '')
    

                if int(nplayer) > 0:
                
                    client.message('^3ID : ^5%s^3 - Server : ^5%s^3 - Player(s) : ^5%s^3 / ^5%s^3'%(str(cid), name, nplayer, slots))

                cursor.moveNext()
            
            c += 1
            
        cursor.close()

                        