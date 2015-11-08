import os
import sys
import cv2
from PIL import Image

# Input file options
INPUT_VIDEO_FOLDER = 'input/'
INPUT_VIDEO_NAME = 'input.mp4'

# Output file options
OUTPUT_FOLDER = 'output/'
OUTPUT_IMAGE_FOLDER = OUTPUT_FOLDER + 'images/'
OUTPUT_IMAGE_FILE = 'output'
OUTPUT_FILE_TYPE = 'PNG'
OUTPUT_IMAGE_WIDTH = 1920
OUTPUT_IMAGE_HEIGHT = 1080

# Various constants
IMAGE_MODE = 'RGB'

def compute_average_image_colors(video_path):
    '''
    Copied from Ayub Khan's answer on StackOverflow:
    http://stackoverflow.com/questions/10672578/extract-video-frames-in-python
    '''
    vc = cv2.VideoCapture(video_path)
    
    if not vc.isOpened():
        print 'Error: Could not open video file: ' + video_path
        sys.exit(1)

    frame_count = int(vc.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

    frame_sample_rate = frame_count / OUTPUT_IMAGE_WIDTH
    
    image_count = 1
    average_image_colors = []
    while True:
        # Read in current frame
        rval, frame = vc.read()

        # If we stop reading data, break out
        if not rval:
            break
        
        # Only sample some images, comment the next line if you want to use every frame
        if image_count % frame_sample_rate == 0:
            img = Image.fromarray(frame)
            img = img.resize((50,50))
            average = compute_average_image_color(img)
            average_image_colors.append(average)

        # This step can take a while, output progress every 10%
        if image_count % (frame_count / 10) == 0 or image_count == frame_count:
            progress = int(image_count / float(frame_count) * 100)
            print '\t' + str(progress) + '% complete'

        # Check for force close/interrupt events
        cv2.waitKey(1) 

        image_count += 1

    vc.release()

    return average_image_colors

def compute_average_image_color(img):
    width, height = img.size

    r_ave = 0
    g_ave = 0
    b_ave = 0

    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x,y))
            r_ave = (r + r_ave) / 2
            g_ave = (g + g_ave) / 2
            b_ave = (b + b_ave) / 2

    return (r_ave, g_ave, b_ave)


def create_image_from_column_colors(column_colors):
    output_image = Image.new(IMAGE_MODE, (len(column_colors), OUTPUT_IMAGE_HEIGHT))

    for column_index in range(len(column_colors)):
        color = column_colors[column_index]
        
        # Fill entire column with same color
        for y in range(OUTPUT_IMAGE_HEIGHT):
            output_image.putpixel((column_index, y), color)

    # If you comment out the sampling code, uncomment the line below
    # return output_image.resize((OUTPUT_IMAGE_WIDTH, OUTPUT_IMAGE_HEIGHT))
    return output_image

# Make sure input file exists
if not os.path.exists(INPUT_VIDEO_FOLDER + INPUT_VIDEO_NAME):
    print 'Error: Input movie file does not exist at location: ' + INPUT_VIDEO_FOLDER + INPUT_VIDEO_NAME
    sys.exit(1)

# Make sure output folder exists
if not os.path.exists(OUTPUT_IMAGE_FOLDER):
    os.makedirs(OUTPUT_IMAGE_FOLDER)

print 'Computing average image colors...'
average_image_colors = compute_average_image_colors(INPUT_VIDEO_FOLDER + INPUT_VIDEO_NAME)

print 'Creating new image...'
output_image = create_image_from_column_colors(average_image_colors)

print 'Saving image...'
output_image_path = OUTPUT_FOLDER + OUTPUT_IMAGE_FILE + '.' + OUTPUT_FILE_TYPE.lower()
output_image.save(output_image_path, OUTPUT_FILE_TYPE)

print 'Image saved as: ' + output_image_path