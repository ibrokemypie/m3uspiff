#!/usr/bin/env python
"""Parse M3U playlists and generate XSPF playlist based on resolved tags."""
from __future__ import print_function
import sys
import subprocess
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


def parse_m3u(m3ufile, playlist):
    """Reads the lines of the input file"""
    track_list = SubElement(playlist, "trackList")
    for line in m3ufile:
        # strip any of the extended m3u ickiness
        if not line.lstrip().startswith('#'):
            # create "track" subtree
            track_element = SubElement(track_list, "track")
            # add location straight away
            location_element = SubElement(track_element, "location")
            location_element.text = line.rstrip()
            # now find the other tags
            mdata(line, track_element)


def mdata(path, track_element):
    """Find the metadata of each accesible file, and format as XML."""
    # Define list of tags to search for
    tags = {"title", "artist", "album", "genre", "recording date", "label"}
    # Define ffprobe syntax
    cmd = ['ffprobe', path.rstrip()]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    # Main loop
    while True:
        out = process.stdout.readline()
        decoded = out.decode('utf-8')
        if out != b'':
            linecheck = decoded.replace(" ", "")
            for tag in tags:
                tagstring = tag+":"
                if tagstring in linecheck:
                    stringf = decoded.split(': ')[1]
                    ttag = tag
                    if tag == "artist":
                        ttag = "creator"
                    if tag == "genre":
                        ttag = "info"
                    ttag = SubElement(track_element, ttag)
                    ttag.text = stringf.rstrip()
        else:
            break


def write_file(m3ufile, playlist):
    """Saves the string of the XML to the new XSPF file."""
    # Create a string from the XML tree
    prettyxml = minidom.parseString(tostring(playlist, 'utf-8'))

    # Create a file with same name and XSPF suffix
    new_file = open(m3ufile+".xspf", "w")

    # Write the final string to the new file
    new_file.write(prettyxml.toprettyxml(indent="  "))
    new_file.close()


def main():
    """Main function"""
    # Require one argument
    if len(sys.argv) != 2:
        print(sys.argv)
        print("Please enter ONE argument", file=sys.stderr)
        sys.exit(1)

    argument = sys.argv[1]

    # Set up XML root and namespace
    playlist = Element("playlist")
    playlist.set("version", "1")
    playlist.set("xmlns", "http://xspf.org/ns/0/")

    # Open the given file first, then give file object
    with open(argument) as m3ufile:
        parse_m3u(m3ufile, playlist)

    write_file(argument, playlist)


if __name__ == '__main__':
    main()
