from PIL import Image
from PIL.ExifTags import TAGS
from glob import glob
import os
import shutil

# Defining the directory to open
img_dir = "REPLACE THIS WITH THE PATH FOR THE FOLDER IN WHICH YOUR IMAGES IS PLACED"

#Reading through the folder, finding all .JPG files, returning a list
image_files = glob(f'{img_dir}/*.JPG')

# Empty list which will be used to store dates, extracted from the images exifdata
dates_list = []

#Loop looks through each image in list
for image_file in image_files:

    # Opens each image
    img = Image.open(image_file)

    # Extracts the exifdata
    exifdata = img.getexif()

    # Looks through the data tags
    for tagid in exifdata:

        #Gets the tags
        tagname = TAGS.get(tagid, tagid)

        #Gets the values
        value = exifdata.get(tagid)

        #Says that we only want the tag if it is called DateTime, DateTimeOriginal or DateTimeDigitized
        if tagname == 'DateTime' or tagname == 'DateTimeOriginal' or tagname == 'DateTimeDigitized':

            # Looks at the values for the tagname, and splits them, as we only want the specific date, not the time
            split_value = value.split(' ')

            # Stores the dates only in a variable
            value_date = split_value[0]

            #Closes image so that it is not kept open by python
            img.close()
            # Checks to see if the date is already in the dates list, and if it is not, it adds the value to the list, giving us a list of unique dates
            if value_date not in dates_list:
                dates_list.append(value_date)
                print(dates_list)

#Transforms all instances of ":" to "-" in order to use right syntax for folder creation
trans_table = str.maketrans(":","-")
dates_list_formatted = [s.translate(trans_table) for s in dates_list]

print(dates_list_formatted)


# Runs through all the dates in the list
for date in dates_list_formatted:

    # Creates a new folder in the image folder, based on the date
    try:
        os.makedirs(os.path.join(img_dir, date))
        print(f"Directory {date} created sucesfully.")

    # Gives an error message, if the folder already exist
    except FileExistsError:
        print(f"Directory {date} already exists.")

    # Gives an error message, if acces to the folder is denied
    except PermissionError:
        print(f"Permission denied: Unable to create '{date}'.")

    # Gives an error message for other errors
    except Exception as e:
        print(f"An error occurred: {e}")


#Loop looks through each image in list again, this time it is to be able to compare exifdata with the created folders
for image_file in image_files:

    # Opens each image
    img = Image.open(image_file)

    # Extracts the exifdata
    exifdata = img.getexif()

    # Looks through the data tags
    for tagid in exifdata:

        #Gets the tags
        tagname = TAGS.get(tagid, tagid)

        #Gets the values
        value = exifdata.get(tagid)

        #Says that we only want the tag if it is called DateTime, DateTimeOriginal or DateTimeDigitized
        if tagname == 'DateTime' or tagname == 'DateTimeOriginal' or tagname == 'DateTimeDigitized':

            # Looks at the values for the tagname, and splits them, as we only want the specific date, not the time
            split_value = value.split(' ')

            # Stores the dates only in a variable
            value_date = split_value[0]

            # Formats the value, so that it can be compared with the foldernames
            trans_table = str.maketrans(":","-")
            formatted_exifdata = value_date.translate(trans_table)

            #Defines the destination folder which images should be send to
            destination_folder = os.path.join(img_dir, formatted_exifdata)

            #Closes image so that it is not kept open by python
            img.close()

            #Moves images to the destinationfolder, based on the dates
            shutil.move(image_file, destination_folder)

            
            


