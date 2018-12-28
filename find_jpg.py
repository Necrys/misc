#!/usr/bin/python

import os
import os.path
import datetime
import shutil
import PIL.Image, PIL.ExifTags

def find_jpg_with_creation_date(folder, copy_to):
    result = []
    for root, dirnames, filenames in os.walk(folder):
        for f in filenames:
            if not (f.lower().endswith("jpg") or f.lower().endswith("jpeg")):
                continue
            fpath = os.path.join(root, f)
            try:
                img = PIL.Image.open(fpath)
                if img.format != "JPEG":
                    continue
                exifdata = img._getexif()
                if exifdata is None:
                    continue
                exif = {
                    PIL.ExifTags.TAGS[k]: v
                    for k, v in exifdata.items()
                    if k in PIL.ExifTags.TAGS
                }
                if "DateTime" not in exif and "DateTimeOriginal" not in exif:
                    result.append(fpath)
                    to_fpath = os.path.join(copy_to, "unsorted")
                
                    if not os.path.exists(to_fpath):
                        os.makedirs(to_fpath)
                    
                    to_fpath = os.path.join(to_fpath, f)
                    if os.path.exists(to_fpath):
                        continue
                    shutil.copyfile(fpath, to_fpath)
                elif "DateTimeOriginal" in exif:
                    exif_date_str = exif["DateTimeOriginal"]
                elif "DateTime" in exif:
                    exif_date_str = exif["DateTimeOriginal"]

                exif_date = datetime.datetime.strptime(exif_date_str, "%Y:%m:%d %H:%M:%S")

                print "Found suitable file at '{}'".format(fpath)
                result.append(fpath)
                
                to_fpath = os.path.join(copy_to, str(exif_date.year))
                to_fpath = os.path.join(to_fpath, str(exif_date.month).zfill(2))
                to_fpath = os.path.join(to_fpath, str(exif_date.day).zfill(2))
                
                if not os.path.exists(to_fpath):
                    os.makedirs(to_fpath)
                
                to_fpath = os.path.join(to_fpath, f)
                if os.path.exists(to_fpath):
                    continue
                shutil.copyfile(fpath, to_fpath)
            except Exception as e:
                print "Exception caught: {}".format(e)
                continue

        #for d in dirnames:
        #    result += find_jpg_with_creation_date(os.path.join(dirname, d), date_from, date_to)
    return result

if __name__ == "__main__":
    DATE_FROM = datetime.datetime(2018, 06, 01)
    DATE_TO = datetime.datetime(2018, 07, 01)
    files = find_jpg_with_creation_date("./", "./copied")
    print "Found {} files".format(len(files))
