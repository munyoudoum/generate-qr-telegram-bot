import qrcode

def create_qr(text) -> None:
    """Create QR from the user message."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    # img = Image.open('img.png')
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)

    tmp_filename = "tmp_qrcode.webp"
    img.save(tmp_filename)

if __name__ == "__main__":
    create_qr('123456')