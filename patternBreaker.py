from typing import List, Optional, Set
from basicDataSet import BasicDataSet
from pattern import Pattern
from debugger import Debugger


class PatternBreaker:
    def __init__(self, dataset_path: str, threshold: float ,interestedIndexes: Optional[List[int]] = None, debug: Optional[bool] = False):
        
        self.dataset = BasicDataSet(dataset_path, interestedIndexes)
        self.threshold = threshold
        if debug:
            self.debugger = Debugger()

    def find_max_uncovered_pattern_set(self) -> List[Pattern]:
        if self.debugger:
            self.debugger.setTimeBegin()
        
        mups: Set[Pattern] = set()

        # Create the root pattern
        root = Pattern.get_root_pattern(self.dataset.getDimension())

        cur_pattern_level = [root] # List of MUPs candidates
        prev_pattern_set = [root] # List of MUPs candidates from the previous level - level i-1
        next_pattern_set = [] # List of MUPs candidates for the next level - level i+1

        # Top-down traversal to find MUPS
        while cur_pattern_level:
            patterns_to_remove = set() # Set to optimize the removal of patterns from the current_set

            for current_pattern in cur_pattern_level:
                if(current_pattern == Pattern([6,4,1,0])):
                    print("Found")
                # Generate parent patterns
                parents_of_cur_pattern = current_pattern.gen_parents()

                # Check if this pattern could still be a MUP
                if_possibly_mup = True
                for parent_pattern in parents_of_cur_pattern:
                    # If any parent is in the MUPS set or not in prev_pattern_set(pruned), 
                    # then current_pattern can't be a MUP
                    cov = self.dataset.checkCoverage(parent_pattern)
                    if parent_pattern in mups or parent_pattern not in prev_pattern_set:
                        if_possibly_mup = False
                        break

                if not if_possibly_mup:
                    patterns_to_remove.add(current_pattern)
                    continue

                # Check coverage threshold
                self.debugger.increment_node_visited()
                if self.dataset.checkCoverage(current_pattern) < self.threshold:
                    assert current_pattern not in mups  # Sanity (debug)
                    mups.add(current_pattern)
                    self.debugger.increment_mups()
                else:
                    # Expand the pattern by replacing positions after the right-most deterministic index
                    generated_children = current_pattern.gen_children(self.dataset,True) # Rule 1
                    next_pattern_set.extend(generated_children)

            # Remove patterns that cannot be MUPS
            cur_pattern_level = [pattern for pattern in cur_pattern_level if pattern not in patterns_to_remove]
            # The current set becomes the 'previous' set in the next iteration
            prev_pattern_set = cur_pattern_level
            # Move all newly created patterns into the current set
            cur_pattern_level = next_pattern_set
            next_pattern_set = []
        
        if self.debugger:
            self.debugger.end()

        return mups
