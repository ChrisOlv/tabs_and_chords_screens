# tabs_and_chords_screens
This Python scrip takes screenshot of tabs / chords from music websites

## How does it work ? 
* On windows, execute the chords.bat
* paste the webpage url
* Script takes a screen shot of the webpage (technically speaking, it takes only the specific <div> from the html page)
* saves it to your computer. You can change the `markdown_dir` and `image_dir`
* creates a markdown file
* integrates the image and fill metadata :

## Metadata :
Artist is [[ surrounded ]] in order to be recognize as local link in Obsidian.
``` md
title: {song_name}
artiste: "[[{artist}]]"
date: {current_date}
```

## Reco
I recommand using a local markdown software to read and organize your tabs. I personnaly prefer Obsidian, but it's up to you.

