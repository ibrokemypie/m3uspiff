#!/usr/bin/env python
"""Parse M3U playlists and generate XSPF playlist based on resolved tags."""
import sys
import subprocess
from lxml import etree

#Require one argument
if len(sys.argv) != 2:
    print str(sys.argv)
    raise NameError('Please enter ONE argument')

#create xml containing playlist and tracklist
playlist = etree.Element("playlist")
playlist.set("version", "1")
playlist.set("xmlns", "http://xspf.org/ns/0/")
trackList = etree.SubElement(playlist, "trackList")

#metadata function
def mdata(path):
    """Find the metadata of each accesible file, and format as XML."""
    #Define list of tags to search for
    tags = {"title", "artist", "album", "genre", "recording date", "label"}
    #Define ffprobe syntax
    cmd = ['ffprobe', path.rstrip()]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #Main loop
    while True:
        out = process.stdout.readline()
        if out != b'':
            linecheck = out.replace(" ", "")
            for tag in tags:
                tagString = tag+":"
                if tagString in linecheck:
                    stringf = out.split(': ')[1]
                    ttag = tag
                    if tag == "artist":
                        ttag = "creator"
                    if tag == "genre":
                        ttag = "info"
                    ttag = etree.SubElement(trackT, tag)
                    ttag.text = stringf.rstrip()
        else:
            break

#get lines from input file
for line in open(sys.argv[1]):
    #strip any of the extended m3u ickiness
    if not line.lstrip().startswith('#'):
        #create "track" subtree
        trackT = etree.SubElement(trackList, "track")
        #add location straight away
        locationT = etree.SubElement(trackT, "location")
        locationT.text = line.rstrip()
        #now find the other tags
        mdata(line)

#save the final xspf to file
tree = etree.tostring(playlist, xml_declaration=True, encoding="utf-8", pretty_print=True)
newFile = open(sys.argv[1]+".xspf", "w")
newFile.write(tree)
newFile.close()
