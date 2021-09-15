from crossword import *

set1 = {1, 2, 3}
set2 = {2}


sample_dict = {
	"1": 2,
	"2": 1
}

list1 = sorted(sample_dict.items(), key=lambda item: item[1])
list2 = [x for (x, y) in list1]



