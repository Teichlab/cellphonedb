import numpy as np
import pandas as pd
from fbpca import pca
from geosketch import gs

from cellphonedb.src.core.core_logger import core_logger


class Subsampler(object):
    def __init__(self, log: bool, num_pc: int = 100, num_cells_ratio: float = 1 / 3, num_cells: int = None):
        self.log = log
        self.num_pc = num_pc
        self.num_cells_ratio = num_cells_ratio
        self.num_cells = num_cells

    def subsample(self, counts: pd.DataFrame) -> pd.DataFrame:
        if self.num_cells is None:
            self.num_cells = int(len(counts) * self.num_cells_ratio)

        core_logger.info('Subsampling {} to {}'.format(len(counts), self.num_cells))

        if self.log:
            pca_input = np.log1p(counts)
        else:
            pca_input = counts

        u, s, vt = pca(pca_input.values, k=self.num_pc)
        x_dimred = u[:, :self.num_pc] * s[:self.num_pc]
        sketch_index = gs(x_dimred, self.num_cells, replace=False)
        x_matrix = counts.iloc[sketch_index]

        core_logger.info('Done subsampling {} to {}'.format(len(counts), self.num_cells))

        return x_matrix
