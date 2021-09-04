import heapq

""""""""""""""""""""""""""
#     Dorin Keshales
#       313298424
""""""""""""""""""""""""""


class PriorityQueue:

    """
    This class implements a priority queue using a priority function received as input. Each item in the priority queue
    is of type Node. Every Node inserted to the queue has priority composed of 3 values: the score given by the priority
    function, it's creation time and the priority of the action from which the node was created.
    """

    def __init__(self, f):

        self.heap = []
        self.f = f

    # Push a node into the priority queue while saving it's creation time and action priority from which created.
    def push(self, item, creation_time, action_priority):
        heapq.heappush(self.heap, (self.f(item), creation_time, action_priority, item))

    # Pop the node with higher f priority and return it.
    def pop(self):

        if self.heap:
            return heapq.heappop(self.heap)[3]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    # Returns whether the item is the queue or not.
    def __contains__(self, item):

        for _, _, _, cur_item in self.heap:
            if cur_item == item:
                return True

        return False

    # Returns the requested item if exists. Otherwise, raise a KeyError exception.
    def __getitem__(self, key):

        for func_score, _, _, item in self.heap:
            if item == key:
                return func_score

        raise KeyError(str(key) + " is not in the priority queue")

    # Removes the requested item if exists. Otherwise, raise a KeyError exception.
    def __delitem__(self, key):

        try:
            del self.heap[[item == key for _, _, _, item in self.heap].index(True)]

        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")

        heapq.heapify(self.heap)

    # Representation of the queue.
    def __repr__(self):
        return str(self.heap)
