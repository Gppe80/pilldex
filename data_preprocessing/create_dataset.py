nimport csv
import os
import errno
import shutil

sorted_csv = '/home/ruifgmonteiro/Desktop/ALTER/sorted_gtt.csv'
csv_with_labels = '/home/ruifgmonteiro/Desktop/ALTER/gtt_with_labels.csv'
database = '/home/ruifgmonteiro/Desktop/ALTER/final_database.csv'

dr = '/home/ruifgmonteiro/Desktop/ALTER/dr'
dc = '/home/ruifgmonteiro/Desktop/ALTER/dc'
train = '/home/ruifgmonteiro/Desktop/ALTER/train'

# Takes a sorted ground truth table (sorted_gtt.csv) and adds the labels to the respective reference
# and consumer images. Returns a list with the following pattern: [ref_image | cons_image | class]

def preprocess_csv(file):
    
    with open(sorted_csv, 'r') as f:
        reader = csv.reader(f, delimiter=',')

        ref_images = []
        cons_images = []
        labels = []
        total = []
        csv_row = 0
        label = 1
        r = 0

        for row in reader:
            if csv_row > 0:
                ref_img = row[0]
                cons_img = row[1]
                ref_images.append(ref_img)
                cons_images.append(cons_img)
                if csv_row > 1:
                    labels.append(label)
            csv_row += 1

            if csv_row > 2:
                if ref_images[r] == ref_images[r - 1]:
                    r += 1
                else:
                    if ref_images[r][36:] == ref_images[r-1][36:]:
                        r += 1
                    else:
                        label += 1
                        labels[r] = label
                        r += 1

        for (a, b, c) in zip(ref_images, cons_images, labels):
            comb = [a, b, c]
            total.append(comb)

    return total

# Writes the list returned by the previous function and writes it to a new csv: gtt_with_labels.

def write_new_csv(file):
    #new_file = '/home/ruifgmonteiro/Desktop/csv_desenvolvimentos/CSV_Handling/gtt_with_labels.csv'
    old_csv_list = preprocess_csv(sorted_csv)
    with open(csv_with_labels, 'w', newline='') as newCsv:
        csv_writer = csv.writer(newCsv)
        csv_writer.writerows(old_csv_list)
    print('Writing completed.')

    return newCsv

# Receives a manipulated csv (final_database.csv) with the 7000 images and respective labels as input.
# Creates 1000 train folders (1 for each class 1 ... 1000)
# Moves 7000 images to their respective directories.

def create_dataset(file):

    # Creates the train directories for classes 1 ... 1000
    if os.path.exists(train) == False:
        os.mkdir(train)

    for index in range(1, 1001):
        try:
            class_dir = os.path.join(train, str(index))
            os.makedirs(class_dir)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    # Reads csv and appends it to a list
    img_folder_list = []
    with open(database, 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        for i in csv_reader:
            img_folder_list.append(i)

    # Moves the images from source folders (dc or dr) to respective train folders
    for file in img_folder_list:
        if file[0] in os.listdir(dr):
            print(str(file[0]) + " exists in dr.")
            shutil.move(os.path.join(dr, str(file[0])), os.path.join(train,str(file[1]),str(file[0])))
            print(str(file[0]) + " has been moved with success.")
        elif file[0] in os.listdir(dc):
            print(str(file[0]) +" exists in dc.")
            shutil.move(os.path.join(dc, str(file[0])), os.path.join(train, str(file[1]), str(file[0])))
            print(str(file[0]) + " has been moved with success.")
        else:
            print("Error: " + str(file[0]) + " does not exist in the specified directories.")

if __name__ == '__main__':
    write_new_csv(sorted_csv)
    create_dataset(database)
