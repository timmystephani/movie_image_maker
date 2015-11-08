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

def convert_video_to_images(video_path, output_folder):
    '''
    Copied from Ayub Khan's answer on StackOverflow
    http://stackoverflow.com/questions/10672578/extract-video-frames-in-python
    '''
    vc = cv2.VideoCapture(video_path)
    
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    image_count = 1
    while rval:
        rval, frame = vc.read()
        cv2.imwrite(output_folder + str(image_count) + '.' + OUTPUT_FILE_TYPE.lower(), frame)
        image_count += 1
        cv2.waitKey(1)
        
    vc.release()
    return image_count

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

def compute_average_column_colors(frame_count, image_folder):
    frame_sample_rate = frame_count / OUTPUT_IMAGE_WIDTH

    average_image_colors = []
    for current_frame_index in range(1, frame_count, frame_sample_rate):
        image_path = image_folder + str(current_frame_index) + '.' + OUTPUT_FILE_TYPE.lower()
        print 'Using image: ' + image_path
        img = Image.open(image_path)
        # Scale to 50x50 to speed things up
        img = img.resize((50,50))
            
        average = compute_average_image_color(img)
        average_image_colors.append(average)

    return average_image_colors

def create_image_from_column_colors(column_colors):
    output_image = Image.new(IMAGE_MODE, (len(column_colors), OUTPUT_IMAGE_HEIGHT))

    for column_index in range(len(column_colors)):
        colors = column_colors[column_index]
        
        # Fill entire column with same color
        for y in range(OUTPUT_IMAGE_HEIGHT):
            output_image.putpixel((column_index, y), colors)

    return output_image

# Make sure input file exists
if not os.path.exists(INPUT_VIDEO_FOLDER + INPUT_VIDEO_NAME):
    print 'Error: Input movie file does not exist at location: ' + INPUT_VIDEO_FOLDER + INPUT_VIDEO_NAME
    sys.exit(1)

# Make sure output folder exists and old images are removed
if os.path.exists(OUTPUT_IMAGE_FOLDER):
    for old_file in os.listdir(OUTPUT_IMAGE_FOLDER):
        if os.path.isfile(old_file):
            os.unlink(old_file)
else:
    os.makedirs(OUTPUT_IMAGE_FOLDER)

print 'Converting video to images...'
image_count = convert_video_to_images(INPUT_VIDEO_FOLDER + INPUT_VIDEO_NAME, OUTPUT_IMAGE_FOLDER)

print 'Computing average column colors...'
column_colors = compute_average_column_colors(image_count, OUTPUT_IMAGE_FOLDER)

print 'Creating new image...'
output_image = create_image_from_column_colors(column_colors)

print 'Saving image...'
output_image_path = OUTPUT_FOLDER + OUTPUT_IMAGE_FILE + '.' + OUTPUT_FILE_TYPE.lower()
output_image.save(output_image_path, OUTPUT_FILE_TYPE)

print 'Image saved as: ' + output_image_path
