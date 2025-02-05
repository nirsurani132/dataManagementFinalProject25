from typing import List, Dict, Optional
from copy import deepcopy
from itertools import product

class Pattern:
    """
    Represents a pattern with a sequence of characters and its associated properties.
    """

    def __init__(self, data: List[str], 
                 idx: Optional[int] = None, 
                 chr_to_replace: Optional[str] = None):
        """
        Initializes a Pattern object.

        param data: A list of characters representing the pattern.
        param idx: Index of the character to replace (optional).
        param chr_to_replace: Character to replace at the given index (optional).
        """
        if idx is not None and chr_to_replace is not None:
            self.data = deepcopy(data)
            self.data[idx] = chr_to_replace
        else:
            self.data = deepcopy(data)
        
        self.coverage = -1
        self.level = self.get_level()

    def get_dimension(self) -> int:
        """
        Returns the dimension of the pattern (length of the data).
        """
        return len(self.data)

    def is_ancestor_of(self, other: 'Pattern') -> bool:
        """
        Checks if the current pattern is an ancestor of the given pattern.

        param other: Another Pattern object.
        return: True if the current pattern is an ancestor of the other pattern, False otherwise.
        """
        if self.get_dimension() != other.get_dimension():
            return False

        for char_self, char_other in zip(self.data, other.data):
            if char_self != 'x' and char_self != char_other:
                return False

        return True

    @staticmethod
    def get_root_pattern(dimension: int) -> 'Pattern':
        """
        Returns the root pattern (all characters are 'x').

        param dimension: Dimension of the pattern.
        return: A root Pattern object.
        """
        root_data = ['x'] * dimension
        return Pattern(root_data)

    def find_right_most_deterministic_index(self) -> int:
        """
        Finds the index of the rightmost deterministic character (non-'x').

        return: The index of the rightmost deterministic character or -1 if none exists.
        """
        for idx in range(self.get_dimension() - 1, -1, -1):
            if self.data[idx] != 'x':
                return idx
        return -1

    def find_right_most_non_deterministic_index(self) -> int:
        """
        Finds the index of the rightmost non-deterministic character ('x').

        :return: The index of the rightmost non-deterministic character or -1 if none exists.
        """
        for idx in range(self.get_dimension() - 1, -1, -1):
            if self.data[idx] == 'x':
                return idx
        return -1

    def gen_parents(self) -> List['Pattern']:
        """
        Generates parent patterns by replacing each non-'x' character with 'x'.

        return: A list of parent patterns.
        """
        parents = []
        for i in range(self.get_dimension()):
            if self.data[i] != 'x':
                    parents.append(Pattern(self.data, i, 'x'))
        return parents
    
    
    def gen_parents_rule2(self) -> List['Pattern']:
        """
        Generates the candidate nodes at level l(P) − 1
        by replacing the deterministic elements with value 0
        in the right-hand side of its right-most non-deterministic element with X
        
        return: A list of parent patterns according to rule 2
        """

        parents = []
        right_most_non_det_idx = self.find_right_most_non_deterministic_index()
        if right_most_non_det_idx == self.get_dimension() - 1:
            return parents
        for i in range(right_most_non_det_idx + 1, self.get_dimension()):
            if self.data[i] == 0:
                parents.append(Pattern(self.data, i, 'x'))
        return parents
    
    
    def get_level(self) -> int:
        """
        return: The level of the pattern (number of deterministic elements).
        """
        return self.get_dimension() - self.data.count('x')

    def __eq__(self, other: object) -> bool:
        """
        Checks equality between two patterns.

        param other: Another object to compare with.
        return: True if both are equal, False otherwise.
        """
        if not isinstance(other, Pattern):
            return False
        return self.data == other.data

    def __hash__(self) -> int:
        """
        Returns the hash value of the pattern.
        """
        return hash(tuple(self.data))

    def __str__(self) -> str:
        """
        Returns a string representation of the pattern, the datatype could be numpy.int64.
        """
        # Convert all elements in self.data to strings
        data_str = ','.join(map(str, self.data))
        return f"{data_str} (cov:{self.coverage})"


    def get_coverage(self) -> int:
        """
        Returns the coverage value of the pattern.
        """
        return self.coverage

    def set_coverage(self, coverage_value: int):
        """
        Sets the coverage value.

        param coverage_value: Coverage value to set.
        """
        self.coverage = coverage_value

        
    def gen_children(self,dataset:'BasicDataSet', rule1 = False) -> List['Pattern']:
        """
        Generates child patterns by replacing one non-deterministic character with a deterministic value.
        rule1: if True, then the children are generated according to rule 1
        ~~otherwise generate all children~~
        
        return: A list of child patterns.
        """
        children = []
        begining_idx = self.find_right_most_deterministic_index() if rule1 else -1
        for i in range(begining_idx + 1,self.get_dimension()):
            if self.data[i] == 'x':
                for value in dataset.getValueRange(i):
                    children.append(Pattern(self.data, i, value))
        return children
    
    def gen_children_rule2(self,dataset:'BasicDataSet') -> List['Pattern']:
        """
        Generates (Partial) list of children patterns at level l(P) + 1,
        Those who create together disjoint partitions of the matches of P,
        by replacing the right-most non-deterministic element with all possible values(See PatternCombiner alg)
        
        return: A (Partial) list of child patterns
        """
        children = []
        right_most_non_det_idx = self.find_right_most_non_deterministic_index()
        if right_most_non_det_idx == -1:
            return children
        for value in dataset.getValueRange(right_most_non_det_idx):
            children.append(Pattern(self.data, right_most_non_det_idx, value))
        return children


    @staticmethod
    def get_all_determinictic_patterns(dataset: 'BasicDataSet') -> List['Pattern']:
        """
        Generates all deterministic patterns from a given dataset

        return: A list of all deterministic patterns.
        """
        attributes_lists = [dataset.getValueRange(0)] # Assuming there is at least one attribute
        for column_idx in range(1, dataset.getDimension()):
            attributes_lists.append(dataset.getValueRange(column_idx))
        product_list = product(*attributes_lists)
        return [Pattern(list(p)) for p in product_list]

        

