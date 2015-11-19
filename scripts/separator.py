import os

print("Starting separator: \n")

my_path = "../dataset"
new_path = "chunks"
chunk_dir = os.path.join(my_path,new_path)

files = [f for f in os.listdir(my_path) if os.path.isfile(os.path.join(my_path, f))]

for f in files:
    if f == 'test_review.json':
        if not os.path.exists(chunk_dir):
            os.makedirs(chunk_dir)

        chunk_size = 4
        smallfile = None
        fid = 0

        with open(os.path.join(my_path, f)) as bigfile:
            for lineno, line in enumerate(bigfile):
                if lineno % chunk_size == 0:
                    if smallfile:
                        smallfile.close()
                    fid += 1
                    small_filename = os.path.join(chunk_dir, 'review_file_{}.json'.format(fid))
                    smallfile = open(small_filename, "w")
                smallfile.write(line)
            if smallfile:
                smallfile.close()