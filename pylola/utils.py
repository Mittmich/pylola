from multiprocessing import Pool
from functools import partial
import bioframe as bf
import pandas as pd
import numpy as np
from scipy.stats import fisher_exact

PSEUDOCOUNT = 10 ** -300


def _get_contingency_table(target, query, universe):
    """calculates contingency table for query, target and universe"""
    query_target = bf.count_overlaps(query, target)
    universe_target = bf.count_overlaps(universe, target)
    a = len(query_target.query("count > 0"))
    b = len(universe_target.query("count > 0")) - a
    c = len(query_target.query("count == 0"))
    d = len(universe) - a - b - c
    return {"a": a, "b": b, "c": c, "d": d}


def _do_enrichment_analysis(row):
    """runs enrichment analysis on contingency table"""
    table = np.array([[row["a"], row["b"]], [row["c"], row["d"]]])
    odds_ratio, p_value = fisher_exact(table, alternative="greater")
    return {
        "odds_ratio": odds_ratio,
        "p_value_log": (-1) * np.log10(p_value + PSEUDOCOUNT),
    }


def run_lola(query, target_list, universe, names=None, processes=2):
    """runs enrichment analysis on query with dataframes in target_list
    spanning the universe."""
    with Pool(processes) as p:
        contingency_list = p.map(
            partial(_get_contingency_table, query=query, universe=universe), target_list
        )
    contingency_frame = pd.DataFrame(contingency_list)
    enrichment_result = contingency_frame.apply(
        _do_enrichment_analysis, axis=1, result_type="expand"
    )
    if names is None:
        return pd.concat((contingency_frame, enrichment_result), axis=1)
    else:
        name_frame = pd.DataFrame({"names": names})
        return pd.concat((contingency_frame, enrichment_result, name_frame), axis=1)
