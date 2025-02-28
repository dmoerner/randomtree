import random
from collections import deque

"""
Cracking the Coding Interview, 4.11:

Implement a binary tree class which, in addition to insert, find, and delete,
has a method `getRandomNode()` which returns a random node from the tree.
All nodes should be equally likely to be chosen.

Shouldn't there be someway to do this with dependency injection into
an existing tree class?

Let's assume there's no duplicates.
"""
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        """
        Print the preorder traversal
        """
        result = []
        def helper(tree: TreeNode):
            result.append(tree.val)
            if tree.left:
                helper(tree.left)
            if tree.right:
                helper(tree.right)
        helper(self)
        return str(result)

    def find(self, target):
        if self.val == target:
            return True
        left = right = False
        if self.left:
            left = self.left.find(target)
        if self.right:
            right = self.right.find(target)

        return left or right

    def insert(self, val):
        if self.left is None:
            self.left = self.__class__(val)
        elif self.right is None:
            self.right = self.__class__(val)
        else:
            subtree = random.choice([self.left, self.right])
            subtree.__class__.insert(subtree, val)


    def deleterec(self, val, parent=None):
        """
        Unfinished, totally recursive implementation of deleterec for use
        with inheritance. Assumes tree has no duplicates.
        """
        if not self:
            return
        if self.val == val:
            if parent is None:
                raise ValueError("can't delete from singleton tree")
            # delete
            return
        if self.left:
            self.__class__.deleterec(self.left, val, self)
        if self.right:
            self.__class__.deleterec(self.right, val, self)


    def delete(self, val):
        """
        Since the tree can have duplicate values, this is not easy to do
        recursively. Use a BFS to delete the first instance found.
        """
        def updateparent(parentptr, dir, target):
            if dir == 0:
                parentptr.left = target
            else:
                parentptr.right = target

        queue = deque([(self, None, 0)])
        while queue:
            cur, parent, dir = queue.popleft()
            if cur.val == val:
                if parent is None:
                    if self.left and self.left.find(val):
                        self.left.__class__.delete(self.left, val)
                        return
                    elif self.right and self.right.find(val):
                        self.right.__class__.delete(self.right, val)
                        return
                    else:
                        raise ValueError("can't delete from singleton tree")
                else:
                    if cur.left is not None and cur.right is not None:
                        cur.val, cur.left.val = cur.left.val, cur.val
                        cur.left.__class__.delete(cur.left, val)
                    elif cur.left is not None:
                        updateparent(parent, dir, cur.left)
                    elif cur.right is not None:
                        updateparent(parent, dir, cur.right)
                    else:
                        updateparent(parent, dir, None)
                    return
            if cur.left:
                queue.append((cur.left, cur, 0))
            if cur.right:
                queue.append((cur.right, cur, 1))



class RandomNode(TreeNode):
    def __init__(self, val, left=None, right=None):
        super().__init__(val, left, right)
        self.size = 1

    def insert(self, val):
        self.size += 1
        super().insert(val)

    def delete(self, val):
        # This doesn't work, right? Yeah, this won't work, because
        # delete is not recursive in the right way.
        self.size -= 1
        super().delete(val)

    def getRandomNode(self):
        pass
