from operator import itemgetter

testa = [(0,4),(0,-2),(0,5),(0,-2)]
sorted_test = sorted(testa, key=itemgetter(1))
print(sorted_test)