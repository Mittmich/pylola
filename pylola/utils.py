import bioframe as bf
import pandas as pd
import numpy as np
from scipy.stats import fisher_exact

def _get_contingency_table(target, query, universe):
    """calculates contingency table for query, target and universe"""
    query_target = bf.count_overlaps(query, target)
    universe_target = bf.count_overlaps(universe, target)
    a = len(query_target.query("count > 0"))
    b = len(universe_target.query("count > 0")) - a
    c = len(query_target.query("count == 0"))
    d = len(universe) - a - b- c
    return {
        "a": a,
        "b": b,
        "c": c,
        "d": d
    }

def _do_enrichment_analysis(row):
    """runs enrichment analysis on contingency table"""
    table = np.array([[
        row["a"], row["b"]
    ], [
        row["c"], row["d"]
    ]])
    odds_ratio, p_value = fisher_exact(table)
    return {
        "odds_ratio": odds_ratio,
        "p_value": p_value
    }

def run_lola(query, target_list, universe, name_series=None):
    """runs enrichment analysis on query with dataframes in target_list
    spanning the universe."""
    contingency_frame = pd.DataFrame([_get_contingency_table(query, target, universe) for target in target_list])
    enrichment_result = contingency_frame.apply(_do_enrichment_analysis, axis=1, result_type="expand")
    if name_series is None:
        return pd.concat((contingency_frame, enrichment_result), axis=1)
    else:
        return pd.concat((contingency_frame, enrichment_result, name_series), axis=1)