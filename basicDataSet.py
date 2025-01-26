from typing import List
import pandas as pd
from pattern import Pattern

class BasicDataSet:
    def __init__(self, dataset_path: str, interestedIndexes: List[int]):
        self.data = pd.read_csv(dataset_path).dropna().iloc[:, interestedIndexes] if interestedIndexes else pd.read_csv(dataset_path).dropna()
        self.mapping = BasicDataSet.preprocess_data(self.data)
        self.cardinalities = [len(self.data.iloc[:,i].unique()) for i in range(len(self.data.columns))]
        self.attributesNames = self.data.columns
        self.dim = len(self.data.columns)
        self.size = len(self.data)

    @staticmethod
    def preprocess_data(data: pd.DataFrame):
        # Create an empty dictionary to store mappings for each column
        mappings = {}

        # Iterate over each column and map its values to integers
        for col in data.columns:
            # Get unique values and create a mapping dictionary
            unique_vals = data[col].unique()
            mappings[col] = {val: idx for idx, val in enumerate(unique_vals)}
            
            # Map the column values to integers using the mapping
            data[col] = data[col].map(mappings[col])
        
        return mappings

    
    def getDimension(self) -> int:
        return self.dim
    
    def getValueRange(self, idx: int) -> List[str]:
        return list(self.data.iloc[:, idx].unique())


    def checkCoverage(self,pattern:Pattern) -> float:
        # if the pattern is the root pattern, then it covers the whole dataset
        if(pattern == pattern.get_root_pattern(self.dim)):
            pattern.set_coverage(self.size)
            return self.size 
        

        # Get indexes of the attributes that are not 'x'
        non_x_indexes = [i for i in range(len(pattern.data)) if pattern.data[i] != 'x']
        projected_data = self.data.iloc[:, non_x_indexes]
        projected_pattern = [pattern.data[i] for i in non_x_indexes]

        # get number of rows in the projected data that match the pattern
        pattern.set_coverage((projected_data == projected_pattern).all(axis=1).sum())
        return pattern.coverage
