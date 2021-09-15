words = ['was', 'when', 'where', 'was']

cant = ['was']

for word in words:
	if word in cant:
		words.remove('was')

print(words)
