from Node import *
class BST:
    def __init__(self, root):
        self.root = root

    def insert(self, val):
        curr = self.root

        while True:
            if val > curr.val:
                if curr.right is None:
                    curr.right = Node(val)
                    return
                else:
                    curr = curr.right
            else:
                if curr.left is None:
                    curr.left = Node(val)
                    return
                else:
                    curr = curr.left

    def delete(self, val):
        def delete_node(node, val):
            if node is None:
                return node

            if val < node.val:
                node.left = delete_node(node.left, val)
            elif val > node.val:
                node.right = delete_node(node.right, val)
            else:
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left

                temp = self.min_value_node(node.right)
                node.val = temp.val
                node.right = delete_node(node.right, temp.val)

            return node

        self.root = delete_node(self.root, val)

    def min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def max_value_node(self, node):
        current = node
        while current.right is not None:
            current = current.right
        return current

    def inorder(self):
        result = []

        def traverse(node):
            if node.left:
                traverse(node.left)
            result.append(node)
            if node.right:
                traverse(node.right)

        traverse(self.root)
        return result

    def balance(self):
        def balance_bst(nodes):
            if not nodes:
                return None

            mid = len(nodes) // 2
            root = nodes[mid]
            root.left = balance_bst(nodes[:mid])
            root.right = balance_bst(nodes[mid + 1:])

            return root

        self.root = balance_bst(self.inorder())


drzewo = BST(Node(10))
drzewo.insert(5)
drzewo.insert(11)
drzewo.insert(15)
drzewo.insert(7)
drzewo.insert(12)
drzewo.balance()
drzewo.delete(11)

print(drzewo.inorder())