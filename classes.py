import cfscrape,requests,json,sqlite3
import discord
from sqlite3 import Error
from datetime import datetime, date, timedelta


session = requests.Session()
session.headers = ...
scraper = cfscrape.create_scraper(sess=session)

class cfxBot:
    def __init_(self):
        print('CFX Init')

    def createEmbed(self,title,fields):
        embed = discord.Embed(title = title,colour = 000000)
        for _ in fields:
            embed.add_field(name = fields[_]['name'], value = fields[_]['content'], inline = False)

        return embed

    def formatName(self,content):
        filter = ['^0','^1','^2','^3','^4','^5','^6','^7','^8','^9']
        for _ in filter: content = content.replace(_,'')
        return content

    def cfxInformation(self,cfxCode):
        cfxRequest = scraper.get('https://servers-live.fivem.net/api/servers/single/' + cfxCode)
        
        if cfxRequest.status_code == 200:
            cfxJson = json.loads(cfxRequest.text)

            try:
                cfxName = cfxJson['Data']['hostname']
                cfxAddress = cfxJson['Data']['connectEndPoints'][0]
            except:
                return 'Error'

            if 'cfx' in cfxAddress:
                cfxRequest = scraper.post(cfxAddress + 'client', data={'method': 'getEndpoints','token': 'youdontneedatoken'})
                cfxAddress = json.loads(cfxRequest.text)[0]

            ipRequest = scraper.get('http://ip-api.com/json/' + cfxAddress.split(':')[0])
            cfxIsp,cfxLocation = json.loads(ipRequest.text)['isp'],json.loads(ipRequest.text)['country']

            return {
                'Name' : self.formatName(cfxName),
                'IP' : cfxAddress.split(':')[0],
                'Port' : cfxAddress.split(':')[1],
                'Location' : cfxLocation,
                'ISP' : cfxIsp
            }

        else:
            return 'Error'

    def openConnection(self):
        try:
            global connection
            global cursor
            connection = sqlite3.connect('cfx.db')
            cursor = connection.cursor()
        except:
            print('Error on database connection')
            return
    
    def whitelistCheck(self,id,role):
        self.openConnection()
        cursor.execute('SELECT * FROM cfx WHERE ID = %d' % id)
        try:
            ID,Admin,Subscription,Expiration = cursor.fetchone()
        except:
            return False

        if role == 'admin' and Admin == 'true':
            return True

        elif role == 'subscriber' and Subscription == 'true':
            if Expiration == 'Never':
                return True

            expdate = datetime.strptime(Expiration,"%d/%m/%Y").date()
            now = date.today()
            if now > expdate:
                cursor.execute("DELETE FROM cfx WHERE ID = %d" % id)
                connection.commit()
                return False
            else:
                return True

    def getExpiration(self,id): 
        self.openConnection()       
        cursor.execute('SELECT * FROM cfx WHERE ID = %d' % id)
        try:
            ID,Admin,Subscription,Expiration = cursor.fetchone()
            return Expiration
        except:
            return False
        
    def addUser(self,id,exp):
        self.openConnection()
        if self.userExists(id) == False:
            cursor.execute("INSERT INTO cfx (ID,Admin,Subscription,Expiration) VALUES ('%d','false','true','%s')" % (id, exp))
            connection.commit()
        else:
            cursor.execute("UPDATE cfx SET ID = '%d',Subscription = '%s',Expiration = '%s'" % (id,'true',exp))
            connection.commit()

    def removeUser(self,id):
        self.openConnection()
        if self.userExists(id) == True:
            cursor.execute("DELETE FROM cfx WHERE ID = %d" % id)
            connection.commit()

    def userExists(self,id):
        self.openConnection()
        cursor.execute("SELECT ID FROM cfx WHERE ID = %d" % id)
        user = cursor.fetchone()
        if not (user == None):
            return True
        return False

    def lookupIp(self,ip):
        lookup = scraper.get('http://ip-api.com/json/%s' % ip)
        lookupInfo = json.loads(lookup.text)

        if lookupInfo['status'] == 'success':
            return lookupInfo
        else:
            return False

            
