import math


def printField(field):
	print ''
	for x in field:
		print x
	print ''


def sumAdjacent(field, x, y):
	sum = 0

	for i in range(x - 1, x + 2):
		for j in range(y - 1, y + 2):
			# print 'Checking: ' + str(i) + ', ' + str(j)
			if not (x == i and y == j):
				sum = sum + getValueIfInField(field, i, j)

	return sum


def getValueIfInField(field, x, y):
	if x < 0 or y < 0:
		return 0
	else:
		try:
			return field[x][y]
		except:
			return 0


num = 361527
# num = 25

sqrt = int(math.sqrt(math.sqrt(num))) / 2

field = [0] * sqrt
for i in range(sqrt):
	field[i] = [0] * sqrt

originOffset = sqrt / 2
field[originOffset][originOffset] = 1
printField(field)

curX = originOffset
curY = originOffset + 1
curNum = 2
lastNum = 1
curEdge = 1
while (lastNum <= num):
	lastNum = sumAdjacent(field, curX, curY)
	field[curX][curY] = lastNum
	curNum = curNum + 1

	# printField(field)
	while curY < originOffset + curEdge:
		curY = curY + 1
		lastNum = sumAdjacent(field, curX, curY)
		field[curX][curY] = lastNum
		curNum = curNum + 1

	# printField(field)
	while curX > originOffset - curEdge:
		curX = curX - 1
		lastNum = sumAdjacent(field, curX, curY)
		field[curX][curY] = lastNum
		curNum = curNum + 1

	# printField(field)
	while curY > originOffset - curEdge:
		curY = curY - 1
		lastNum = sumAdjacent(field, curX, curY)
		field[curX][curY] = lastNum
		curNum = curNum + 1

	# printField(field)
	while curX < originOffset + curEdge:
		curX = curX + 1
		lastNum = sumAdjacent(field, curX, curY)
		field[curX][curY] = lastNum
		curNum = curNum + 1

	curEdge = curEdge + 1


printField(field)