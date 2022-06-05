import skimage
from PIL import Image, ImageChops, ImageFilter, ImageEnhance
import os
import random


def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)

    # Mit 3. Parameter spielen für Ausschnitt, 4. für Größe
    diff = ImageChops.add(diff, diff, 0.5, -100)

    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def trimimages():
    directory = r'MillPictures/Raw/'
    cropDirectory = r'MillPictures/Cropped/'
    cnt = 0

    for filename in os.listdir(directory):
        # Case sensitive! Klein ebenfalls hinzufügen.
        if filename.endswith(".JPG") or filename.endswith(".jpg"):
            factor = random.uniform(0.5, 1.5)
            im = Image.open(os.path.join(directory, filename))

            im = trim(im)
            # im.show()
            im.save(cropDirectory + str(cnt) + ".jpg")

            # Für Filter

            imFlip = im.transpose(Image.FLIP_LEFT_RIGHT)
            imFlip.save(cropDirectory + str(cnt) + "Flip" + ".jpg")

            imBlur = im.filter(ImageFilter.GaussianBlur)
            imBlur.save(cropDirectory + str(cnt) + "Blur" + ".jpg")

            imSharp = im.filter(ImageFilter.SHARPEN)
            imSharp.save(cropDirectory + str(cnt) + "Sharp" + ".jpg")

            # Für Enhancer

            enhancerBrightness = ImageEnhance.Brightness(im)
            imBrightness = enhancerBrightness.enhance(factor)
            imBrightness.save(cropDirectory + str(cnt) + "Brightness" + ".jpg")

            enhancerContrast = ImageEnhance.Contrast(im)
            imContrast = enhancerContrast.enhance(factor)
            imContrast.save(cropDirectory + str(cnt) + "Contrast" + ".jpg")

            cnt += 1
        else:
            continue


if __name__ == "__main__":
    trimimages()

# OpenCV:
# https://docs.opencv.org/3.4/d4/d70/tutorial_hough_circle.html
