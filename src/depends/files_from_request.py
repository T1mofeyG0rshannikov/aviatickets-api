import csv
from io import StringIO

from fastapi import File, UploadFile


async def get_csv_file(
    csv_file: UploadFile = File(...),
):
    contents = await csv_file.read()
    decoded_contents = contents.decode("utf-8")

    csv_file = StringIO(decoded_contents)
    csv_data = csv.reader(csv_file)

    csvinput = []
    for row in csv_data:
        csvinput.append(row)

    return csvinput


async def get_txt_file(
    txt_file: UploadFile = File(...),
):
    contents = await txt_file.read()
    decoded_contents = contents.decode("utf-8")

    strings = []

    for line in decoded_contents.splitlines():
        if len(line) > 1:
            strings.append(line)

    return strings
