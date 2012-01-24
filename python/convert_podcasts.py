#!/usr/bin/python
'''
Created on Jun 23, 2011

@author: nick
'''

import os
import re
import sys
from subprocess import call

# no speedup
SPEEDUP_0 = ["wait wait"]

#25% speedup
SPEEDUP_25 = ["freakonomics",
              "radiolab",
              "this american life",
	      "planet money",
	      "how to do everything"]

#50% speedup
SPEEDUP_50 = ["floss weekly",
              "security now",
              "tech news today",
	      "news summary",
	      "marketplace tech report",
	      "on science"]

SOCK_FILE = '/tmp/podcast_socket'

#def opensocket():
#    if (os.access(SOCK_FILE, os.F_OK)):
#        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#	try:
#	    socket.connect(SOCK_FILE)
#	    socket.send()
#	except:
#	    
#    
#    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#    try:
#    	os.remove('/tmp/podcast_socket')
#    except OSError:
#    	pass
#    s.bind('/tmp/podcast_socket')
#    s.listen(1)
#    conn, addr = s.accept()
#    data = conn.recv(1024)
#    conn.close()

def getfileinfo():
    fileinfo = {}
    fileinfo['url'] = os.environ.get("GPODDER_EPISODE_URL", "")
    fileinfo['episode'] = os.environ.get("GPODDER_EPISODE_TITLE", "")
    fileinfo['filename'] = os.environ.get("GPODDER_EPISODE_FILENAME", "")
    fileinfo['extension'] = os.path.splitext(fileinfo['filename'])[1]
    fileinfo['date'] = os.environ.get("GPODDER_EPISODE_PUBDATE", "")
    fileinfo['link'] = os.environ.get("GPODDER_EPISODE_LINK", "")
    fileinfo['description'] = os.environ.get("GPODDER_EPISODE_DESC", "")
    fileinfo['channel'] = os.environ.get("GPODDER_CHANNEL_TITLE", "")
    return fileinfo

def soundstretch(filename, tempo):
    filenames = {'base': filename, 'wav': filename + '.wav',
                 'fast': filename + '.fast.wav', 'final': filename + '.2.mp3',
                 'backup': filename + '.bak'}
    
    # Decode mp3 to wav
    call(['lame', '--decode', filenames['base'], filenames['wav']])
    
    # Call soundstretch to convert wav
    call(['soundstretch', filenames['wav'], filenames['fast'], '-speech',
          '-tempo=+' + tempo])
    
    # Encode stretched wav back to mp3
    call(['lame', '--preset', 'fast', 'standard', filenames['fast'],
          filenames['final']])
    
    # Copy id3 tags to new mp3
    call(['id3cp', filenames['base'], filenames['final']])
    
    # Move final mp3 to new name original
    os.rename(filenames['base'], filenames['backup'])
    os.rename(filenames['final'], filenames['base'])
    
    # Finally, remove backups/temporary files
    os.remove(filenames['wav'])
    os.remove(filenames['fast'])
    os.remove(filenames['backup'])
    
def gettempo(channelname):
    lowerchannel = channelname.lower()
    if re.search('|'.join(SPEEDUP_0), lowerchannel):
        return '0'
    elif re.search('|'.join(SPEEDUP_25), lowerchannel):
        return '35'
    elif re.search('|'.join(SPEEDUP_50), lowerchannel):
        return '60'
    else:
        return '0'

#TODO: Switch all tagging to id3v2?
def fixid3(fileinfo):
    call(['id3tag',
          '-a', fileinfo['channel'], # Overwrite unicode tags (mojibake)
          '-A', fileinfo['channel'],
          '-t1', # TODO: Something other than 1 for podcasts that tr# matters
          '-s', fileinfo['episode'],
          fileinfo['filename']])
    # id3tag does not support non-numeric genres
    call(['id3v2',
          '-g', 'Podcast'])
    
# If files are specified on the command line, just adjust speed based on rules
if __name__ == '__main__':
    if(sys.argv[1:]):
        # TODO: Use this to modify existing files
        print "Not supporting command line params yet" 
    else:
        fileinfo = getfileinfo()
        if fileinfo['extension'] == '.mp3':
            fixid3(fileinfo)
            tempo = gettempo(fileinfo['channel'])
            if tempo != '0':
                soundstretch(fileinfo['filename'], tempo)


