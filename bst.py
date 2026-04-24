from __future__ import annotations

class Node:
    def __init__(
            self,
            value: int ,
            parent: Node | None = None,
            left: Node | None = None,
            right: Node | None = None
    ):
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right

    def __repr__(self):
        return str(self.value)


class BSTTree:
    def __init__(self):
        self.root = None

    def _sibling(self, node: Node):
        parent = node.parent
        if parent == None:
            return None
        return parent.left if parent.right == node else parent.right

    def _locate_parent(self, node: Node):

        current = self.root
        parent = None

        while current != None:
            parent = current
            if node.value < current.value:
                current = current.left
            else:
                current = current.right
        
        return parent
    


    def _greatest(self, node: Node):
        
        while node.right != None:
            node = node.right
        return node


    def insert(self, value: int):
        node = Node(value)

        parent = self._locate_parent(node)
        node.parent = parent

        if parent == None:
            self.root = node
            return
        elif node.value < parent.value:
            parent.left = node
        else:
            parent.right = node

    def delete(self, value: int):
        z = self.search(value)
        if z == None:
            return

        if z.left != None and z.right != None:
            pred = self._greatest(z.left)
            z.value = pred.value
            z = pred

        x = z.left if z.left != None else z.right

        if z.parent == None:
            self.root = x
        elif z == z.parent.left:
            z.parent.left = x
        else:
            z.parent.right = x
        if x != None:
            x.parent = z.parent

                

    def search(self, value: int):
        current = self.root
        while current != None and current.value != value:
            if current.value > value:
                current = current.left
            else:
                current = current.right
        return current
    

    def traverse(self):
        result = []
        def _split(node: Node | None):
            if node == None:
                return
            _split(node.left)
            result.append(node.value)
            _split(node.right)
        _split(self.root)
        return result


def draw(tree: BSTTree):
    layer = [tree.root]
    
    while len(layer) != 0:
        print(layer)
        new_layer = []
        for node in layer:
            if node != None:
                new_layer.append(node.left)
                new_layer.append(node.right)

        layer = new_layer





    

