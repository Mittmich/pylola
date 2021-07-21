import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
import pylola


class TestRunLOLA(unittest.TestCase):
    """Tests for the run_lola functions."""
    @classmethod
    def setUp(self):
        self.query1 = pd.read_csv("./tests/test_files/query1.bed", sep="\t", header=None)[[0, 1, 2]].rename(columns={0: "chrom", 1: "start", 2: "end"})
        self.target1 = pd.read_csv("./tests/test_files/target1.bed", sep="\t")[["chrom", "start", "end"]]
        self.target2 = pd.read_csv("./tests/test_files/target2.bed", sep="\t", header=None)[[0, 1, 2]].rename(columns={0: "chrom", 1: "start", 2: "end"})
        self.target_list = [self.target1, self.target2]
        self.universe = pd.concat((self.query1, self.target1, self.target2)).reset_index(drop=True)

    def test_regions_subsets_of_universe(self):
        """Compares that output of the R LOLA version with pylola 
        where query and targets are a subset of universe."""
        result = pylola.run_lola(self.query1, self.target_list, self.universe, processes=1)
        expected = pd.DataFrame({
            "a": [39596, 27201],
            "b": [69997, 71404],
            "c": [919, 13314],
            "d": [1409, 2],
            "p_value_log": [0.0001901352, 0.0000],
            "odds_ratio": [0.8673024, 6.1035 * 10**-5],
        })
        assert_frame_equal(result, expected)


if __name__ == "__main__":
    res = unittest.main(verbosity=3, exit=False)