# m3uspiff
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/ca3c7e99191f4f07b354945ff9108628/badge.svg)](https://www.quantifiedcode.com/app/project/ca3c7e99191f4f07b354945ff9108628)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

An M3U to XSPF playlist converter.

## Usage
``./m3uspiff.py [playlist.m3u]``

Converts M3U format playlists into XSPF (XML Shareable Playlist Format) playlists, using FFMPEG's ffprobe to augment the new playlist with each included song's metadata when available.

## Requirements
* python2

* ffmpeg