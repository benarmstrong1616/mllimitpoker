import sys
import pickle
import copy

#simple script used to check the contents of strategy files
#script is also used to count the number of entries in the file that aren't None
count_pickle = "n"
file_name = sys.argv[1]
if(len(sys.argv) > 2):
    count_pickle = sys.argv[2]
pickle_file = open(file_name, 'rb')
f = pickle.load(pickle_file)
not_none = 0
if(count_pickle.upper() == "Y"):
    for a in range(8):
        for b in range(9):
            for c in range(20):
                for d in range(3):
                    for e in range(5):
                        if f[a][b][c][d][e]:
                            not_none = not_none + 1
    print(not_none)
else:
    print(f)