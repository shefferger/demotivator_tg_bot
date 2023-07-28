from PIL import Image, ImageOps, ImageDraw, ImageFont
import textwrap
import io


def make_demotivator(img: bytes, text: str):
    pimg = Image.open(fp=io.BytesIO(img))
    for i in pimg.size:
        if i < 100:
            return None
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
    borders = (round(min_size / 20), round(min_size / 20), round(min_size / 20), round(min_size / 20))
    pimg = ImageOps.expand(pimg, border=borders, fill='black')
    font_size = round(min_size / 10)
    font = ImageFont.truetype('timesnewroman.ttf', font_size)
    current_h, pad = pimg.height - round(min_size / 21), 2
    para = textwrap.wrap(text=text, width=23)
    for line in para:
        draw = ImageDraw.Draw(pimg)
        w, h = draw.textsize(text=line, font=font)
        borders = (0, 0, 0, h)
        pimg = ImageOps.expand(pimg, border=borders, fill='black')
        draw = ImageDraw.Draw(pimg)
        draw.text(((pimg.width - w) / 2, current_h), line, font=font, fill=(255, 255, 255))
        current_h += h + pad
    buffer = io.BytesIO()
    pimg.save(fp=buffer, format=file_type)
    return buffer.getvalue()


def test():
    with open(mode='rb', file='samples/test.png') as fd:
        file = fd.read()
        img = make_demotivator(img=file, text='hello world! yay! its a good day today, isnt it? i really like it ')
        with open(mode='wb', file='/mnt/c/Users/sheff/Desktop/res/sample-out.png') as fd2:
            fd2.write(img)


if __name__ == '__main__':
    test()
