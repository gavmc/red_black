from __future__ import annotations

class Node:
    def __init__(
            self,
            value: int ,
            color: str = "r",
            parent: Node | None = None,
            left: Node | None = None,
            right: Node | None = None
    ):
        self.value = value
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{str(self.value)}{str(self.color)}"


class Tree:
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
    
    
    def _left_rotate(self, node: Node):

        root = node.right
        root.parent = node.parent
        node.parent = root

        temp = root.left
        node.right = temp
        if temp != None:
            temp.parent = node
        root.left = node

        if root.parent != None:
            if node == root.parent.left:
                root.parent.left = root
            else:
                root.parent.right = root
        else:
            self.root = root


    def _right_rotate(self, node: Node):
        
        root = node.left
        root.parent = node.parent
        node.parent = root

        temp = root.right
        node.left = temp
        if temp != None:
            temp.parent = node
        root.right = node

        if root.parent != None:
            if node == root.parent.left:
                root.parent.left = root
            else:
                root.parent.right = root
        else:
            self.root = root


    def _insert_fix(self, node: Node):
        while node != self.root and node.parent.color == "r":
            parent = node.parent
            gran = parent.parent
            if gran == None:
                break
            uncle = self._sibling(parent)

            if uncle != None and uncle.color == "r":
                parent.color = "b"
                uncle.color = "b"
                gran.color = "r"
                node = gran
            else:
                if node == parent.right and parent == gran.left:
                    self._left_rotate(parent)
                    node = parent          
                    parent = node.parent
                elif node == parent.left and parent == gran.right:
                    self._right_rotate(parent)
                    node = parent
                    parent = node.parent

                parent.color = "b"
                gran.color = "r"
                if parent == gran.left:
                    self._right_rotate(gran)
                else:
                    self._left_rotate(gran)
                break  

        self.root.color = "b"

    def _greatest(self, node: Node):
        
        while node.right != None:
            node = node.right
        return node


    def _delete_fix(self, x: Node | None, x_parent: Node | None):
        while x != self.root and (x == None or x.color == "b"):
            if x == x_parent.left:
                w = x_parent.right

                if w.color == "r":
                    w.color = "b"
                    x_parent.color = "r"
                    self._left_rotate(x_parent)
                    w = x_parent.right

                if (w.left == None or w.left.color == "b") and (w.right == None or w.right.color == "b"):
                    w.color = "r"
                    x = x_parent
                    x_parent = x.parent
                else:
                    if w.right == None or w.right.color == "b":
                        w.left.color = "b"
                        w.color = "r"
                        self._right_rotate(w)
                        w = x_parent.right

                    w.color = x_parent.color
                    x_parent.color = "b"
                    w.right.color = "b"
                    self._left_rotate(x_parent)
                    x = self.root 
            else:
                w = x_parent.left

                if w.color == "r":
                    w.color = "b"
                    x_parent.color = "r"
                    self._right_rotate(x_parent)
                    w = x_parent.left

                if (w.left == None or w.left.color == "b") and \
                (w.right == None or w.right.color == "b"):
                    w.color = "r"
                    x = x_parent
                    x_parent = x.parent
                else:
                    if w.left == None or w.left.color == "b":
                        w.right.color = "b"
                        w.color = "r"
                        self._left_rotate(w)
                        w = x_parent.left

                    w.color = x_parent.color
                    x_parent.color = "b"
                    w.left.color = "b"
                    self._right_rotate(x_parent)
                    x = self.root

        if x != None:
            x.color = "b"


    def insert(self, value: int):
        node = Node(value)

        parent = self._locate_parent(node)
        node.parent = parent

        if parent == None:
            self.root = node
            self.root.color = "b"
            return
        elif node.value < parent.value:
            parent.left = node
        else:
            parent.right = node

        self._insert_fix(node)

    def delete(self, value: int):
        z = self.search(value)
        if z == None:
            return

        if z.left != None and z.right != None:
            pred = self._greatest(z.left)
            z.value = pred.value
            z = pred

        removed_color = z.color
        x = z.left if z.left != None else z.right
        x_parent = z.parent

        if z.parent == None:
            self.root = x
        elif z == z.parent.left:
            z.parent.left = x
        else:
            z.parent.right = x
        if x != None:
            x.parent = z.parent

        if removed_color == "b":
            self._delete_fix(x, x_parent)
                

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


def draw(tree: Tree):
    layer = [tree.root]
    
    while len(layer) != 0:
        print(layer)
        new_layer = []
        for node in layer:
            if node != None:
                new_layer.append(node.left)
                new_layer.append(node.right)

        layer = new_layer

