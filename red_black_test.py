import numpy as np
from tqdm import tqdm
import time
import matplotlib.pyplot as plt
import sys

from red_black import Tree, Node
from bst import BSTTree


class TestSuite:
    def __init__(self, tree_class):
        self.tree_class = tree_class
        self.tree = tree_class()

    def reset(self):
        self.tree = self.tree_class()

    def _validate(self):

        def _check_bh(node):
            if node == None:
                return 0, 0, 0
            
            val1, h1, n1 = _check_bh(node.left)
            val2, h2, n2 = _check_bh(node.right)

            assert val1 == val2, "uneven black height"

            if node.color == "b":
                val1 += 1

            return val1, max(h1, h2)+1, n1+n2+1
        
        def _check_bst(node, low=None, high=None):
            
            if node == None:
                return
            
            assert low == None or node.value >= low
            assert high == None or node.value <= high
                    
            _check_bst(node.left, low, node.value)
            _check_bst(node.right, node.value, high)

        def _check_double_red(node):
            if node == None:
                return
            
            if node.color == "r":
                assert node.left == None or node.left.color == "b", "double red"
                assert node.right == None or node.right.color == "b", "double red"
                
            _check_double_red(node.left)
            _check_double_red(node.right)
                
        assert self.tree.root == None or self.tree.root.color == "b"
        
        bh, h, n = _check_bh(self.tree.root)
        _check_bst(self.tree.root)
        _check_double_red(self.tree.root)

        assert bh >= (h/2), "broke bn >= h/2"
        assert n >= np.power(2, bh)-1, "broke n >= (2^bh)-1"
        assert h <= 2*np.log2(n+1), "broke h <= 2log(n+1)"
        assert bh <= np.log2(n+1), "broke bh <= log(n+1)"
        

    def search_tests(self):
        self.reset()
        assert self.tree.search(5) == None

        self.tree.insert(10)
        assert self.tree.search(10) != None and self.tree.search(10).value == 10
        assert self.tree.search(5) == None

        for num in [1, 5, 8, 23, 7, 9]:
            self.tree.insert(num)
        for num in [1, 5, 8, 23, 7, 9, 10]:
            search = self.tree.search(num)
            assert search != None and search.value == num
        for num in [-3, 0, 24, 85]:
            assert self.tree.search(num) == None

    def traverse_test(self):
        self.reset()
        assert self.tree.traverse() == []

        for i in range(5):
            self.reset()
            val = [i for i in range(200)]
            np.random.shuffle(val)

            for num in val:
                self.tree.insert(num)

            assert self.tree.traverse() == sorted(val), f"{self.tree.traverse()}\n{sorted(val)}"
            

    def insert_sorted_diag(self):
        self.reset()
        for num in range(100):
            self.tree.insert(num)
            self._validate()

        assert self.tree.traverse() == [i for i in range(100)]
        self.reset()

        for num in range(99, -1, -1):
            self.tree.insert(num)
            self._validate()

        assert self.tree.traverse() == [i for i in range(100)]


    def insert_duplicate(self):
        self.reset()

        for num in [2, 2, 2, 2, 2]:
            self.tree.insert(num)
            self._validate()

        assert self.tree.traverse() == [2, 2, 2, 2, 2]
        self.reset()

        for num in [2, 3, 2, 3, 2, 3]:
            self.tree.insert(num)
            self._validate()

        assert self.tree.traverse() == sorted([2, 3, 2, 3, 2, 3])

    def delete_empty(self):
        self.reset()
        self.tree.delete(5)
        assert self.tree.root == None

    def delete_nonexistant(self):
        self.reset()
        self.tree.insert(5)
        self.tree.insert(10)
        self.tree.delete(7)
        self._validate()
        assert self.tree.traverse() == [5, 10]

    def delete_root(self):
        self.reset()
        self.tree.insert(5)
        self.tree.delete(5)
        assert self.tree.root == None
        assert self.tree.traverse() == []

    def delete_red_end(self):
        self.reset()
        for num in [10, 5, 15]:
            self.tree.insert(num)

        self.tree.delete(5)
        self._validate()
        assert self.tree.traverse() == [10, 15]

    def delete_black_end(self):
        self.reset()

        for num in [10, 5, 15, 20]:
            self.tree.insert(num)

        self.tree.delete(5)
        self._validate()
        assert self.tree.traverse() == [10, 15, 20]

    def delete_single_child(self):
        self.reset()

        for num in [10, 5, 15, 20]:
            self.tree.insert(num)

        self.tree.delete(15)
        self._validate()
        assert self.tree.traverse() == [5, 10, 20]

    def delete_two_child(self):
        self.reset()

        for num in [2, 4, 6, 8, 10]:
            self.tree.insert(num)
        
        self.tree.delete(8)
        self._validate()
        assert self.tree.traverse() == [2, 4, 6, 10]

    def delete_root(self):
        self.reset()

        rem_order = [4, 3, 2, 6, 5, 8, 7, 1, 9]

        temp = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for num in temp:
            self.tree.insert(num)

        
        for num in rem_order:
            self.tree.delete(num)
            self._validate()
            temp.remove(num)
            assert self.tree.traverse() == temp

        assert self.tree.root == None
        

    def stress_test(self, n=10000, max_val=200):
        self.reset()
        items = []

        for i in tqdm(range(n)):
            inp = np.random.randint(0, 6)
            val = np.random.randint(0, max_val)

            if inp < 3:
                self.tree.insert(val)
                items.append(val)
            elif inp < 5:
                self.tree.delete(val)
                if val in items:
                    items.remove(val)
            else:
                search = self.tree.search(val)
                if val in items:
                    assert search != None and search.value == val
                else:
                    assert search == None

            self._validate()
            assert self.tree.traverse() == sorted(items)



    def run_test(self):
        print("Search tests ---")
        self.search_tests()
        print("Traverse tests ---")
        self.traverse_test()
        print("Insert tests ---")
        self.insert_sorted_diag()
        self.insert_duplicate()
        print("Delete tests ---")
        self.delete_empty()
        self.delete_nonexistant()
        self.delete_root()
        self.delete_red_end()
        self.delete_black_end()
        self.delete_single_child()
        self.delete_two_child()
        self.delete_root()
        print("Stress test ---")
        self.stress_test()



    def _run_perf_test(self, tree):
        scales = [10000, 100000, 300000, 1000000, 3000000, 10000000]
        trials = 2
        
        scores_insert = []
        scores_search = []
        scores_traverse = []
        scores_delete = []
        
        for n in scales:
            t_ins = 0
            t_srch = 0
            t_trav = 0
            t_del = 0
            
            for _ in range(trials):
                current_tree = tree()
                values = [i for i in range(n)]
                
                np.random.shuffle(values)
                start = time.perf_counter()
                for num in values:
                    current_tree.insert(num)
                t_ins += (time.perf_counter() - start) / n
                
                np.random.shuffle(values)
                start = time.perf_counter()
                for num in values:
                    current_tree.search(num)
                t_srch += (time.perf_counter() - start) / n
                
                start = time.perf_counter()
                for _ in range(10):
                    current_tree.traverse()
                t_trav += (time.perf_counter() - start) / 10
                
                np.random.shuffle(values)
                start = time.perf_counter()
                for num in values:
                    current_tree.delete(num)
                t_del += (time.perf_counter() - start) / n
            
            scores_insert.append(t_ins / trials)
            scores_search.append(t_srch / trials)
            scores_traverse.append(t_trav / trials)
            scores_delete.append(t_del / trials)
            
            print(f"n={n:>7}  ins={scores_insert[-1]*1e6:.2f}µs  "
                f"srch={scores_search[-1]*1e6:.2f}µs  "
                f"trav={scores_traverse[-1]*1e3:.2f}ms  "
                f"del={scores_delete[-1]*1e6:.2f}µs")
        
        _, axes = plt.subplots(2, 2, figsize=(10, 8))

        axes[0, 0].plot(scales, scores_insert, marker="o", color="C0")
        axes[0, 0].set_title("Insert")
        axes[0, 0].set_xlabel("Items")
        axes[0, 0].set_ylabel("Time (s)")
        axes[0, 0].grid(True, alpha=0.3)

        axes[0, 1].plot(scales, scores_search, marker="o", color="C1")
        axes[0, 1].set_title("Search")
        axes[0, 1].set_xlabel("Items")
        axes[0, 1].set_ylabel("Time (s)")
        axes[0, 1].grid(True, alpha=0.3)

        axes[1, 0].plot(scales, scores_delete, marker="o", color="C2")
        axes[1, 0].set_title("Delete")
        axes[1, 0].set_xlabel("Items")
        axes[1, 0].set_ylabel("Time (s)")
        axes[1, 0].grid(True, alpha=0.3)

        axes[1, 1].plot(scales, scores_traverse, marker="o", color="C3")
        axes[1, 1].set_title("Traverse")
        axes[1, 1].set_xlabel("Items")
        axes[1, 1].set_ylabel("Time (s)")
        axes[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig("red_black.png", dpi=300) if isinstance(tree(), Tree) else plt.savefig("BST.png", dpi=300)



    def performance_eval(self):
        print("Red-Black Tree:")
        self._run_perf_test(Tree)
        print()
        print("Binary Search Teee:")
        self._run_perf_test(BSTTree)



if __name__ == "__main__":
    
    tests = TestSuite(Tree)
    tests.performance_eval()
