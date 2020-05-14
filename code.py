import collections
import copy


class Node:
    def __init__(self, puzzle, end, parent=None, action=None):
        self.puzzle = puzzle
        self.end = end
        self.parent = parent
        self.action = action
        if (self.parent != None):
            self.g = parent.g + 1
        else:
            self.g = 0

    @property
    def actions(self):
        rows = len(self.puzzle)
        current_node_0_positions = []
        row_number = 0
        for row in self.puzzle:
            column_number = 0
            for column in row:
                if column == 0:
                    current_node_0_positions += [[row_number, column_number]]
                column_number += 1
            row_number += 1
        self.zero_positions= current_node_0_positions
        if self.parent == None:
            parent_node_zero_possitions = []
        else:
            parent_node_zero_possitions = self.parent.zero_positions
        child_nodes = []
        possible_positions = []
        for i in self.zero_positions:
            if (i[0] + 1 < rows) and ([i[0] + 1, i[1]] not in self.zero_positions) and ([i[0] + 1, i[1]] not in parent_node_zero_possitions):
                possible_positions += [[[i[0] + 1, i[1]],'up']]
            if (i[0] - 1 >= 0) and ([i[0] - 1, i[1]] not in self.zero_positions) and ([i[0] - 1, i[1]] not in parent_node_zero_possitions):
                possible_positions += [[[i[0] - 1, i[1]],'down']]
            if (i[1] + 1 < rows) and ([i[0], i[1] + 1] not in self.zero_positions) and ([i[0], i[1] + 1] not in parent_node_zero_possitions):
                possible_positions += [[[i[0], i[1] + 1],'left']]
            if (i[1] - 1 >= 0) and ([i[0], i[1] - 1] not in self.zero_positions) and ([i[0], i[1] - 1] not in parent_node_zero_possitions):
                possible_positions += [[[i[0], i[1] - 1],'right']]
            #if self.parent == None:
                #parent_node_zero_possitions = []
            #else:
                #parent_node_zero_possitions = self.parent.zero_positions
            #for remove_position in parent_node_zero_possitions:
                #try:
                    #possible_positions.remove(remove_position)
                #except:
                    #pass
            for possible_position in possible_positions:
                new_child = copy.deepcopy(self.puzzle)
                new_child[possible_position[0][0]][possible_position[0][1]] = 0
                new_child[i[0]][i[1]] = self.puzzle[possible_position[0][0]][possible_position[0][1]]
                child_nodes+=[[new_child,[self.puzzle[possible_position[0][0]][possible_position[0][1]],possible_position[1]]]]
            possible_positions=[]
        return child_nodes

    @property
    def state(self):
        return str(self)

    @property
    def solved(self):
        return self.puzzle==self.end



    @property
    def h1(self):
        goal_node_positions = {}
        row_number = 0
        for row in self.end:
            column_number = 0
            for column in row:
                goal_node_positions[column] = (row_number, column_number)
                column_number += 1
            row_number += 1
        rows = len(self.puzzle)
        #print(rows)
        #print((self.puzzle))
        distance = 0
        for i in range(rows):
            for j in range(rows):
                if list(self.puzzle)[i][j] != 0:
                    x, y = goal_node_positions[self.puzzle[i][j]]
                    distance += abs(x - i) + abs(y - j)
        return distance



    @property
    def h2(self):
        rows = len(self.puzzle)
        number_of_tiles = 0
        for i in range(rows):
            for j in range(rows):
                if self.end[i][j] != 0 and self.end[i][j] != self.puzzle[i][j]:
                    number_of_tiles += 1
        return number_of_tiles

    @property
    def f1(self):
        return self.h1 + self.g

    @property
    def f2(self):
        return self.h2 + self.g

    @property
    def path(self):
        node=self
        path=[]
        while node.parent !=None:
            #print(node.action)
            #print(node.puzzle[0])
            #print(node.puzzle[1])
            #print(node.puzzle[2])
            #print(node.puzzle[3])
            #print('\n')
            path+=[tuple(node.action)]
            node=node.parent
        path.reverse()
        return path

#a=Node([[1,2,0],[3,4,5],[6,7,8]],[[1,2,3],[4,5,6],[7,8,0]])
#print(a.actions)
#a=Node([[1,0,0],[3,4,5],[6,7,8]],[[1,2,3],[4,5,6],[7,0,0]])
#print(a.actions)

#open=[]


def main(start,end):
    queue = collections.deque([Node(start,end)])
    #print(queue)
    seen = set()
    seen.add(queue[0].state)
    #print(seen)
    while queue:
        queue = collections.deque(sorted(list(queue), key=lambda node: node.f2))
        #print(len(queue))
        node = queue.popleft()
        #print(node.solved)
        if node.solved:
            #print(node.puzzle)
            #print(node.parent)
            #for i in node.path:
                #print(i)
            return node.path

        for action in node.actions:
            #print(action)
            child = Node(action[0],end,node,action[1])

            if child.state not in seen:
                queue.appendleft(child)
                seen.add(child.state)

#print(main([[1,4,0,7],[9,2,3,5],[6,0,10,13],[8,11,14,12]],[[1,4,7,5],[9,2,3,0],[0,11,10,13],[6,8,14,12]]))
#print(main([[1,2,3],[5,6,0],[7,8,4]],[[1,2,3],[5,8,6],[0,7,4]]))
#board = [[1,2,3],[4,5,0],[6,7,8]]
#board = [[5,0,8],[4,2,1],[7,3,6]]
print(main([[5,0,8],[4,2,1],[7,3,6]],[[1,2,3],[4,5,6],[7,8,0]]))

def file_read():
    f = open("Sample_Start_Configuration.txt", "r")

    start=[]
    for i in range(4):
        row=[]
        for j in f.readline().strip().split('\t'):
            if j=='-':
                row+=[0]
            else:
                row+=[int(j)]
        start+=[row]
        row=[]
    #print(start)
    f.close()
    f = open("Sample_Goal_Configuration.txt", "r")

    goal=[]
    for i in range(4):
        row=[]
        for j in f.readline().strip().split('\t'):
            if j=='-':
                row+=[0]
            else:
                row+=[int(j)]
        goal+=[row]
        row=[]
    #print(goal)
    f.close()
    return start,goal
start,goal=file_read()
print(main(start,goal))

#f = open("1.txt", "w")
#f.write(str(main(start,goal))[1:-1])
#f.write(str(main(start,goal)))
#f.close()

f = open("2.txt", "w")
f.write(str(main(start,goal))[1:-1])
#f.write(str(main(start,goal)))
f.close()
