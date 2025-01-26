from typing import List, Optional
from basicDataSet import BasicDataSet
from pattern import Pattern


class PatternBreaker:
    def __init__(self, dataset_path: str, threshold: float, interestedIndexes: Optional[List[int]] = None):
        
        self.dataset = BasicDataSet(dataset_path, interestedIndexes)
        self.threshold = threshold

    def find_max_uncovered_pattern_set(self, threshold) -> set[Pattern]:
        mups = set()

        # Create the root pattern
        root = Pattern.get_root_pattern(self.dataset.getDimension())

        cur_pattern_set = {root}
        prev_pattern_set = set()
        next_pattern_set = set()

        # Top-down traversal to find MUPS
        while cur_pattern_set:
            patterns_to_remove = set()

            for current_pattern in cur_pattern_set:
                # Generate parent patterns
                parents_of_cur_pattern = current_pattern.gen_parents()

                # Check if this pattern could still be a MUP
                if_possibly_mup = True
                for parent_pattern in parents_of_cur_pattern.values():
                    # If any parent is in the MUPS set or not in prev_pattern_set, 
                    # then current_pattern can't be a MUP
                    if parent_pattern in mups or parent_pattern not in prev_pattern_set:
                        if_possibly_mup = False
                        break

                if not if_possibly_mup:
                    patterns_to_remove.add(current_pattern)
                    continue

                # Check coverage threshold
                if self.dataset.checkCoverage(current_pattern) < threshold:
                    mups.add(current_pattern)
                else:
                    # Expand the pattern by replacing positions after the right-most deterministic index
                    right_most_det_idx = current_pattern.find_right_most_deterministic_index()
                    for i in range(right_most_det_idx + 1, current_pattern.get_dimension()):
                        for value_to_replace in self.dataset.getValueRange(i):
                            # Create a new pattern with the updated position
                            next_pattern_set.add(
                                Pattern(current_pattern.data, i, value_to_replace)
                            )

            # Remove patterns that cannot be MUPS
            cur_pattern_set.difference_update(patterns_to_remove)
            # The current set becomes the 'previous' set in the next iteration
            prev_pattern_set = set(cur_pattern_set)
            # Move all newly created patterns into the current set
            cur_pattern_set = set(next_pattern_set)
            next_pattern_set.clear()

        return mups
