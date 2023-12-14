import easyocr
print("---OCR Model loaded---")

def ocr(path):
    reader = easyocr.Reader(['en', 'vi'])
    texts = reader.readtext(path, detail=0)
    
    result = []
    info = ""
    for text in texts:
        info_length = info.count(" ") + 1
        text_length = text.count(" ") + 1

        if info_length + text_length <= 60:
            info = info + text + " "
        else:
            result.append(info)
            info = text + " "
    result.append(info)

    return result