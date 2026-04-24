import pygame as pg
from red_black import Tree


def get_layers(tree):
    layers = []
    current = [tree.root]

    while len(current) > 0:
        layers.append(current)
        temp = current.copy()
        current = []
        for node in temp:
            if node != None:
                current.append(node.left)
                current.append(node.right)

    return layers


def draw_tree(tree):
    layers = get_layers(tree)
    print(layers)

    pg.init()
    font  = pg.font.SysFont("Arial", 20)

    screen = pg.display.set_mode((len(layers)*150, len(layers)*80))

    def _walk(node, pos, layer = 1):
        if node == None:
            return
        
        offset = int(150*(1/(layer)))
        
        if node.left != None:
            pg.draw.line(screen, (100, 100, 100), (pos[0], pos[1]), (pos[0] - offset, pos[1] + 80))
        
        if node.right != None:
            pg.draw.line(screen, (100, 100, 100), (pos[0], pos[1]), (pos[0] + offset, pos[1] + 80))
        
        color = (255, 0, 0) if node.color == "r" else (255, 255, 255)
        pg.draw.circle(screen, color, (pos[0], pos[1]), 20)

        num_surface = font.render(str(node.value), True, (0, 0, 0))
        num_rect = num_surface.get_rect()
        num_rect.center = (pos[0], pos[1])

        screen.blit(num_surface, num_rect)

        _walk(node.left, [pos[0] - offset, pos[1] + 80], layer+1)
        _walk(node.right, [pos[0] + offset, pos[1] + 80], layer+1)

    
    _walk(tree.root, [len(layers)*75, 50])

    pg.display.update()


new_tree = Tree()

new_tree.insert(5)
new_tree.insert(10)
new_tree.insert(15)
new_tree.insert(20)
new_tree.insert(7)
new_tree.insert(12)
new_tree.insert(25)
new_tree.insert(30)
new_tree.insert(2)
new_tree.insert(1)
new_tree.insert(0)
new_tree.insert(6)

draw_tree(new_tree)

while True:
    pass