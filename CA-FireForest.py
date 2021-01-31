import pygame
import numpy as np

class FireSim:
    def __init__(self, prob=0.65, fireOnCorner=False, background=(224,222,224)):
        self.FIRE = 2
        self.TREE = 1
        self.EMPTY = 0
        self.rand = prob
        self.fire_takes_corner = fireOnCorner
        self.background_colour = background
        self.M = 78
        self.matrix = np.zeros(shape=(self.M, self.M),dtype=int)
        self.NB_TREES_INIT, self.NB_TREES_RESTANT = 0,0
        (self.width, self.height) = ((self.M+2)*10, (self.M+2)*10)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('FireForest')
        self.screen.fill(self.background_colour)

    def generate_map(self):
        for i in range(self.M):
            for j in range(self.M):
                r = np.random.uniform()
                if r < self.rand:
                    self.matrix[i][j] = self.TREE
                    self.NB_TREES_INIT+=1
                    self.NB_TREES_RESTANT+=1
        for y in range(10,self.height-10,10):
            for x in range(10,self.width-10,10):
                if self.matrix[y//10-1][x//10-1] == self.TREE:
                    pygame.draw.circle(self.screen,(0,255,0),(x+5,y+5),5)

    def is_corner(self, i,j,fire_pos,fire_takes_corner):
        if fire_takes_corner:
            return False
        if i==fire_pos[0]-1 and j==fire_pos[1]-1:
            return True
        if i==fire_pos[0]+1 and j==fire_pos[1]+1:
            return True
        if i==fire_pos[0]-1 and j==fire_pos[1]+1:
            return True
        if i==fire_pos[0]+1 and j==fire_pos[1]-1:
            return True
        return False

    def run(self):
        self.generate_map()
        pygame.display.flip()
        fire_pos = np.random.randint(low=0, high=self.M, size=2)
        x = fire_pos[0]
        y = fire_pos[1]
        if self.matrix[x][y] == self.TREE:
            self.NB_TREES_RESTANT-=1
        self.matrix[x][y] = self.FIRE
        running = True
        fires = [(x,y)]
        while running and len(fires) > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            new_fires = []
            for fire_pos in fires:
                x_fire = fire_pos[0]
                y_fire = fire_pos[1]
                
                for i in range(x_fire-1,x_fire+2):
                    for j in range(y_fire-1,y_fire+2):
                        if i>=0 and i<self.M and j>=0 and j<self.M and self.matrix[i][j] == self.TREE and not self.is_corner(i,j,(x_fire,y_fire),self.fire_takes_corner):
                            new_fires.append((i,j))
                            self.matrix[i][j] = self.FIRE
                            self.NB_TREES_RESTANT-=1
                self.matrix[x_fire][y_fire] = self.EMPTY
            fires = new_fires
            for y in range(10,self.height-10,10):
                for x in range(10,self.width-10,10):
                    if self.matrix[y//10-1][x//10-1] == self.TREE:
                        pygame.draw.circle(self.screen,(0,204,0),(x+5,y+5),5)
                    if self.matrix[y//10-1][x//10-1] == self.FIRE:
                        pygame.draw.circle(self.screen,(255,0,0),(x+5,y+5),5)
                    if self.matrix[y//10-1][x//10-1] == self.EMPTY:
                        pygame.draw.circle(self.screen,(224,222,224),(x+5,y+5),5)
            pygame.display.flip()
            pygame.time.Clock().tick(40)


app = FireSim()
app.run()
