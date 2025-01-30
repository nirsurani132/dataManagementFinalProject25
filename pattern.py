from typing import List, Dict, Optional
from copy import deepcopy

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

    def gen_parents(self) -> Dict[int, 'Pattern']:
        """
        Generates parent patterns by replacing each non-'x' character with 'x'.

        return: A dictionary mapping replaced position to the parent Pattern.
        """
        parents = {}
        for i in range(self.get_dimension()):
            if self.data[i] != 'x':
                    parents[i] = Pattern(self.data, i, 'x')
        return parents

    def get_level(self) -> int:
        """
        Returns the level of the pattern (number of deterministic elements).
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


    def set_coverage(self, coverage_value: int):
        """
        Sets the coverage value.

        :param coverage_value: Coverage value to set.
        """
        self.coverage = coverage_value

