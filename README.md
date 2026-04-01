# Tabs and chords screens
This Python scrip takes screenshot of tabs / chords from music websites

## How does it work ? 
### Installation 
* clone the repo
* edit the url destination on chord_playwright.py (linux or windows)
* Create a .venv and install requirement (pip install -r requirements.txt)
* option : download and install obsidian to visualise your chords/tabs easily

### What does the script do :
* launch chord_playwright.py 
* paste the webpage url
* The script : 
    * takes a screen shot of the webpage (technically speaking, it takes only the specific <div> from the html page)
    * saves it to your computer.
    * creates a markdown file
    * integrates the image and fill metadata

## Metadata :
Artist is [[ surrounded ]] in order to be recognize as local link in Obsidian.
Properties of the .md file : 

``` md
title: {song_name}
artiste: "[[{artist}]]"
date: {current_date}
tags: guitar/chords
```

