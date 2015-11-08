# Movie Image Maker

## About
After seeing a couple posts on reddit ([link1], [link2]) about converting images to barcodes or posters, I thought I would take a crack at it.

[link1]: <https://www.reddit.com/r/dataisbeautiful/comments/3rb8zi/the_average_color_of_every_frame_of_a_given_movie/>
[link2]: <https://www.reddit.com/r/doctorwho/comments/2xhdxe/i_made_a_movie_barcode_of_the_day_of_the_doctor/>

## How it works
* It works by first converting the movie into individual frames
* Then, based off the desired image width, it samples just enough frames to have 1 frame per pixel of desired image width
* Based off each frame, it computes an average color (RGB)
* After that, it creates a 1 pixel column of each of those average colors in a new image and saves it

## Setup
You need to install pillow and opencv.
On my ubuntu machine, I also needed this for image dependencies:
```sh
$ sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
```

## Run the program
```sh
python main.py
```

## Examples
Suits - Season 5 Episode 5
![Example 1](http://i.imgur.com/SXoZxyK.jpg)
Fun with Dick and Jane
![Example 1](http://i.imgur.com/f3S631A.jpg)

## TODOS
* Add black image gradient (clear in middle, darker on top and bottom)
* Add blur effect