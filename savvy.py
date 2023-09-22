# Savvy Module
# Copyright 2023 Shadow Of Hassen
# Savvy is licensed under the the Lesser GPL License



import subprocess
import threading
import socket
import urllib
import urllib.parse
import urllib.request
import json
import http

DEFAULT_PORT = 8081


urlopen = urllib.request.build_opener(urllib.request.HTTPHandler).open

class Server:
    def __init__(self, port=8081,):
        self.host = socket.gethostbyname('localhost')
        self.port = port
        self.url = 'http://{}:{}'.format(self.host, self.port)+'/v2'
        self.server = None      
    
    def terminate_server(self):
        # Took this from language checker
        error_message = ''
        if self.server is not None:
            try:
                self.server.terminate()
            except OSError:
                pass
            

            try:
                error_message = self.server.communicate()[1].strip()
            except (IOError, ValueError):
                pass

            try:
                self.server.stdout.close()
            except IOError:
                pass
            self.server = None

        
    def _consume(self, stdout): # TODO: A les kututhu sounding name???
        while stdout.readline():
            pass
        
    def start_server(self):
        # I took this bit from the language_checker module
        self.url = 'http://{}:{}'.format(self.host, self.port)+'/v2'
        server_cmd =['java', '-cp', 'LanguageTool/languagetool-server.jar',
                     'org.languagetool.server.HTTPServer', '--port '+(str(self.port))+'allow-origin']
        self.server = subprocess.Popen(server_cmd,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          universal_newlines=True,
                          startupinfo=None
                          )
        if self.server:
            consumer_thread = threading.Thread(
                target=lambda: self._consume(self.server.stdout))
            consumer_thread.start()
        self.active = True
        


class LanguageToolMistake:
    def __init__(self, er):  # er is the raw error. I'm sortening it because i'm going to use it a lot
        self.message = er['message']
        self.short_message  = er['shortMessage']
        self.replacements = []
        for x in er['replacements']:
            self.replacements.append(x['value'])
        self.offset = er['offset']
        self.length = er['length']
        self.type =er['type']['typeName']
        
'''
LanguageToolChecker
This is the checker. it's different than the server.
The server above runs Language tool Java. This talks to the server.
It doesn't even need to use the server above set the url for a different place.
If you aren't using the server the must have the /v2 already in it
'''
class LanguageToolChecker:
    def __init__(self, url=None, language='en-US'):
        if url == None:
            self.server = Server()
            self.server.start_server()
            self.url = self.server.url
        else:
            self.server = None
            self.url = url
        self.language= language
    # TODO: Add disabled rules 
    def check(self, text):
        params = urllib.parse.urlencode({'language':self.language, 'text':text}).encode() # Encode turns it to bytes type object
        # Now we define a short name for something
        data =  urlopen(self.url+'/check',data=params)
        # Now we parse the data.
        for x in data:
            pulled_data = x.decode()   # No clue why it needs to go into a loop before I can get it.
        # Now we must decode it.
        # Language tool uses json so.
        decoded_data = json.loads(pulled_data)
        # Now we check for mistakes
        mistakes = []
        for piece in decoded_data['matches']: # We only need the errors
            mistakes.append(LanguageToolMistake(piece))
            
        return mistakes
    
    def close_checker(self):
        if self.server is not None:
            self.server.terminate_server

    def get_languages(self):
        data = urlopen(self.url+ '/languages')
        for x in data:
            pulled_data = x.decode()   # No clue why it needs to go into a loop before I can get it.
        decoded_data = json.loads(pulled_data)
        languages = []
        for x in decoded_data:
            languages.append((x['name'],x['longCode']))
        return languages
    
if __name__ == '__main__':
    l = LanguageToolChecker()
    d = l.check('''Today's is the day you almost mispelled Captain Jack Spawwow!''')
    for i in d:
        print(i.replacements)
    l.close_checker()