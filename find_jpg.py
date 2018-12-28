#!/usr/bin/python

import os
import os.path
import datetime
import shutil
import PIL.Image, PIL.ExifTags

def copy_to_dir(from_path, to_root, to_dir, filename):
    to_fpath = os.path.join(to_root, to_dir)

    if not os.path.exists(to_fpath):
        os.makedirs(to_fpath)
    
    to_fpath = os.path.join(to_fpath, filename)
    if not os.path.exists(to_fpath):
        shutil.copyfile(from_path, to_fpath)


def find_jpg_with_creation_date(folder, copy_to):
    result = []
    for root, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fpath = os.path.join(root, f)

            if not (f.lower().endswith("jpg") or f.lower().endswith("jpeg")):
                copy_to_dir(fpath, copy_to, "bad_file_ext", f)
                continue
            
            try:
                img = PIL.Image.open(fpath)
                if img.format != "JPEG":
                    copy_to_dir(fpath, copy_to, "bad_img_fmt", f)
                    continue
                exifdata = img._getexif()
                if exifdata is None:
                    copy_to_dir(fpath, copy_to, "bad_exif", f)
                    continue
                exif = {
                    PIL.ExifTags.TAGS[k]: v
                    for k, v in exifdata.items()
                    if k in PIL.ExifTags.TAGS
                }
                if "DateTime" not in exif and "DateTimeOriginal" not in exif:
                    copy_to_dir(fpath, copy_to, "unsorted", f)
                    continue
                elif "DateTimeOriginal" in exif:
                    exif_date_str = exif["DateTimeOriginal"]
                elif "DateTime" in exif:
                    exif_date_str = exif["DateTime"]

                exif_date = datetime.datetime.strptime(exif_date_str, "%Y:%m:%d %H:%M:%S")

                print "Found suitable file at '{}'".format(fpath)
                result.append(fpath)

                to_dir = os.path.join(str(exif_date.year), str(exif_date.month).zfill(2))
                to_dir = os.path.join(to_dir, str(exif_date.day).zfill(2))

                copy_to_dir(fpath, copy_to, to_dir, f)
            except Exception as e:
                print "{0} Exception caught: {1}".format(f, e)
                #result.append(fpath)
                to_fpath = os.path.join(copy_to, "except")
            
                if not os.path.exists(to_fpath):
                    os.makedirs(to_fpath)
                
                to_fpath = os.path.join(to_fpath, f)
                if os.path.exists(to_fpath):
                    continue
                shutil.copyfile(fpath, to_fpath)

                continue

        #for d in dirnames:
        #    result += find_jpg_with_creation_date(os.path.join(dirname, d), date_from, date_to)
    return result

if __name__ == "__main__":
    DATE_FROM = datetime.datetime(2018, 06, 01)
    DATE_TO = datetime.datetime(2018, 07, 01)
    files = find_jpg_with_creation_date("./", "./copied")
    print "Found {} files".format(len(files))
