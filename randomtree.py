"""
Cracking the Coding Interview, 4.11:

Implement a binary tree class which, in addition to insert, find, and delete,
has a method `getRandomNode()` which returns a random node from the tree.
All nodes should be equally likely to be chosen.

The goal is to use this is an opportunity to practice Python inheritance.

We will assume that the binary tree has no duplicates and has a minimum
size of 1.

The type hints are just for show: We really need a Comparable type for
values.
"""
from typing import Any, Self
import random

class TreeNode:
    def __init__(self, val: Any | None = None, left: Self | None = None, right: Self | None = None):
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

    def find(self, target: Any):
        if self.val == target:
            return True
        left = right = False
        if self.left:
            left = self.left.find(target)
        if self.right:
            right = self.right.find(target)
        return left or right

    def insert(self, val: int):
        if self.find(val):
            raise ValueError("Attempted to insert duplicate element")
        if self.left is None:
            self.left = self.__class__(val)
        elif self.right is None:
            self.right = self.__class__(val)
        else:
            subtree = random.choice([self.left, self.right])
            subtree.__class__.insert(subtree, val)


    def delete(self, val: int, parent=None):
        """
        Does nothing if the object is not found.
        """
        def update_parent(parent: Self, deleted: Self, new: Self | None):
            """
            Helper function to update the correct pointer in the parent.
            """
            if parent.left == deleted:
                parent.left = new
            elif parent.right == deleted:
                parent.right = new

        def swap_and_delete(node1: Self, node2: Self):
            """
            Helper function to swap the values of two nodes and then
            delte the second one.
            """
            node1.val, node2.val = node2.val, node1.val
            self.__class__.delete(node1, val, node2)

        if self.val == val:
            # Handle the root by reducing to another case.
            if parent is None:
                if self.left is None and self.right is None:
                    raise ValueError("Can't delete from singleton tree")
                elif self.left is not None:
                    swap_and_delete(self, self.left)
                elif self.right is not None:
                    swap_and_delete(self, self.right)
            # Delete this node, adjusting the tree. There are four cases.
            elif self.left is not None and self.right is not None:
                # As a matter of convention: Swap self and self.left, then delete self.left.
                swap_and_delete(self, self.left)
            elif self.left is not None:
                update_parent(parent, self, self.left)
            elif self.right is not None:
                update_parent(parent, self, self.right)
            else:
                update_parent(parent, self, None)

            return
        if self.left and self.left.find(val):
            self.__class__.delete(self.left, val, self)
        if self.right and self.right.find(val):
            self.__class__.delete(self.right, val, self)



class RandomNode(TreeNode):
    def __init__(self, val: Any, left: Self | None = None, right: Self | None =None):
        super().__init__(val, left, right)
        self.size = 1

    def insert(self, val: Any):
        self.size += 1
        super().insert(val)

    def delete(self, val, parent=None):
        # This still doesn't work in the case where we have to
        # do a swap: We are not updating the size properly.
        # Or are we decrementing twice by accident?
        self.size -= 1
        super().delete(val, parent)

    def getRandomNode(self):
        pass
