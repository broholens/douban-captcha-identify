import uuid
from os import remove
import requests
import enchant
from PIL import Image, ImageFilter
from aip import AipOcr


app_id = '11565085'
api_key = 'dh9pPBqw1H4hQQyPrk4HHVv6'
secret_key = '6mjlcxPsT2NRs7wETIqs3xYBjz0pdyH5'
client = AipOcr(app_id, api_key, secret_key)
d = enchant.Dict('en_US')


def process_image(filename):
    image = Image.open(filename)
    threshold_grey = 25
    image = image.convert('L')
    im2 = Image.new("L", image.size, 255)
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            pix = image.getpixel((x, y))
            if int(pix) > threshold_grey:
                im2.putpixel((x, y), 255)
            else:
                im2.putpixel((x, y), 0)
    im2 = im2.filter(ImageFilter.MedianFilter())
    im2.save(filename)
    return im2


def get_file_content(filename):
    with open(filename, 'rb') as fp:
        return fp.read()


def download_img(filename, url):
    with open(filename, 'wb')as f:
        f.write(requests.get(url).content)


def _recognize_check_img(filename, process_img=False):
    if process_img is True:
        process_image(filename)
    img = get_file_content(filename)
    response = client.basicGeneral(img)
    # words = response.get('words_result', [{}])
    words = response.get('words_result')
    print(words)
    if not words:
        return ''
    word = words[0].get('words', 'zz')
    if d.check(word) is True:
        return word
    return ''


def recognize_file(filename):
    word = _recognize_check_img(filename)
    if not word:
        word = _recognize_check_img(filename, True)
    remove(filename)
    return word


def recognize_url(url):
    filename = str(uuid.uuid4()) + '.png'
    print(filename)
    download_img(filename, url)
    return recognize_file(filename)
