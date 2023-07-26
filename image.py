from PIL import Image, ImageOps
import io


def add_border(img: io.BytesIO):
    pimg = Image.open(fp=img)
    min_size = min(pimg.size)
    pimg = pimg.resize(size=(min_size, min_size))
    pimg = ImageOps.expand(pimg, border=2, fill='black')
    pimg = ImageOps.expand(pimg, border=2, fill='white')
    borders = (round(min_size / 20), round(min_size / 20), round(min_size / 20), round(min_size / 4))
    pimg = ImageOps.expand(pimg, border=borders, fill='black')
    pimg.save('/mnt/c/Users/sheff/Desktop/res/imaged-with-border.png')


def test():
    with open(mode='rb', file='samples/test.png') as fd:
        file = fd.read()
        add_border(io.BytesIO(file))


if __name__ == '__main__':
    test()
