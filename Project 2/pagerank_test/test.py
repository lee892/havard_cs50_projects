import random
from pagerank import *

num = random.randrange(3)

nums = [0, 1, 2]
weights = [0.05, 0.475, 0.475]
probabilities = [0, 0, 0]

test_dict = {"one": 1, "two": 2, "three": 3}
for num in test_dict:
	print(num)

	
for i in range(1000):
	probabilities[random.choices(nums, weights)[0]] += 1


print(probabilities)