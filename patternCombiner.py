from typing import List, Dict, Optional, Set
from basicDataSet import BasicDataSet
from pattern import Pattern
from debugger import Debugger

class PatternCombiner:
    def __init__(self, dataset_path: str, threshold: float, interestedIndexes: Optional[List[int]] = None, debug: Optional[bool] = False):
        
        self.dataset = BasicDataSet(dataset_path, interestedIndexes)
        self.threshold = threshold
        self.debugger = Debugger() if debug else None

    def find_max_uncovered_pattern_set(self) -> List[Pattern]:
        if self.debugger:
            self.debugger.setTimeBegin()
        
        mups: Set[Pattern] = set()
        
        # Create new hash
        count: Dict[Pattern, int] = {}
        # Generate all possible deterministic patterns
        all_possible_deterministic_patterns = Pattern.get_all_determinictic_patterns(self.dataset)
        
        # Check coverage for each pattern
        for pattern in all_possible_deterministic_patterns:
            if self.debugger:
                self.debugger.increment_node_visited()
            cnt = self.dataset.checkCoverage(pattern)
            if cnt < self.threshold:
                count[pattern] = cnt
        
        # Check whether count is empty, i.e. no pattern is below the threshold (fully covered dataset)
        if(len(count) == 0):
            return []
        
        for level in range(self.dataset.getDimension()):
            nextCount: Dict[Pattern, int] = {}
            for pattern in count.keys():
                # Generate parent patterns
                parents_of_cur_pattern = pattern.gen_parents_rule2()
                for parent_pattern in parents_of_cur_pattern:
                   
                    # Generate children that creates disjoint partitions of the matches of parent_pattern
                    children = parent_pattern.gen_children_rule2(self.dataset)
                    
                    # Calculate the coverage of the parent pattern
                    # cov(parent) = sum(cov(child)), for example: cov(1xx) = cov(1x1) + cov(1x0)
                    sum_coverage = 0
                    if self.debugger:
                        self.debugger.increment_node_visited()
                    for child in children:
                        # if one of the children is not in count, then it is
                        # covered, so we'll add the threshold and be covered as well.
                        sum_coverage += count[child] if child in count else self.threshold 
                    parent_pattern.set_coverage(sum_coverage)
                    
                    if sum_coverage < self.threshold:
                        nextCount[parent_pattern] = sum_coverage
                    
            # Iterate over all uncovered patterns in level l
            for pattern in count.keys():
                # If none of the parents of the pattern is in nextCount, then pattern is a MUP (since all of them are covered)
                if len(list(filter(lambda x: x in nextCount, pattern.gen_parents()))) == 0:
                    assert pattern not in mups  # Sanity (debug)
                    mups.add(pattern)
                    if self.debugger:
                        self.debugger.increment_mups()
            
            # check whether nextCount is empty. If so, break.
            if(len(nextCount) == 0):
                break

            # Prepare for the next level, which is level (`level` - 1).
            count = nextCount
        
        if self.debugger:
            self.debugger.end()
        
        return mups
