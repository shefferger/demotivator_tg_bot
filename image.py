from PIL import Image, ImageOps
import io


def make_demotivator(img: bytes, text: str):
    pimg = Image.open(fp=io.BytesIO(img))
    match pimg.mode:
        case 'RGB':
            file_type = 'JPEG'
        case 'RGBA':
            file_type = 'PNG'
        case _:
            file_type = 'PNG'
    min_size = min(pimg.size)
    pimg = pimg.resize(size=(min_size, min_size))
    pimg = ImageOps.expand(pimg, border=2, fill='black')
    pimg = ImageOps.expand(pimg, border=2, fill='white')
    borders = (round(min_size / 20), round(min_size / 20), round(min_size / 20), round(min_size / 4))
    pimg = ImageOps.expand(pimg, border=borders, fill='black')
    buffer = io.BytesIO()
    pimg.save(fp=buffer, format=file_type)
    return buffer.getvalue()


def test():
    with open(mode='rb', file='samples/test.png') as fd:
        file = fd.read()
        make_demotivator(file)


if __name__ == '__main__':
    test()
