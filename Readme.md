# pyLOLA

Python implementation of LOLA (https://doi.org/10.1093/bioinformatics/btv612).

## Installation

You can install this repo via pip as follows:

```
    pip install git+https://github.com/Mittmich/pylola
```

## Usage 

pyLOLA can be used to determine enrichment of a query genomic region with a set of target genomic regions in the context of a region universe (see the [original LOLA paper](https://doi.org/10.1093/bioinformatics/btv612) for more details).

Regions are supplied as `pandas` dataframes and all overlap calculations are performed using `bioframe`.

A typical workflow starts by first loading a query region as follows:

```
    query = pd.read_csv(
            "./tests/test_files/query1.bed", sep="\t", header=None
        )
```

Then, one or more target regions are loaded to calculate enrichment amongst them:

```
    target1 = pd.read_csv(
            "./tests/test_files/target1.bed", sep="\t", header=None
        )

    target2 = pd.read_csv(
            "./tests/test_files/target2.bed", sep="\t", header=None
        )
    
        .
        .
        .
    targetN = pd.read_csv(
            "./tests/test_files/targetN.bed", sep="\t", header=None
        )
```

The "target-database" is constructed by putting these regions into a python iterable, for example a list:

```
    targets = [target1, target2, ..., targetN]
```

Finally, an appropriate universe is loaded that contains all possible regions:

```
    universe = pd.read_csv(
            "./tests/test_files/universe.bed", sep="\t", header=None
        )
```


Enrichment is then calculated using the `pylola.run_lola` function:

```
    result = pylola.run_lola(
            query, target_list, universe
        )
```

`pylola.run_lola` returns a dataframe that contains the flattened contingency table as well as the odds-ratio and negative logarithm of the p-value of region a fisher's exact test:

| a     | b     | c   | d    | odds-ratio | p_value_log  |
|-------|-------|-----|------|------------|--------------|
| 39596 | 69998 | 919 | 1409 | 0.8673024  | 0.0001901352 |
| .     | .     | .    | .   | .          | .            |
| .     | .     | .    | .   | .          | .            |
| .     | .     | .    | .   | .          | .            |

The mapping to the respective contingency table is as follows:

|                  | present in target | absent in target |
|------------------|-------------------|------------------|
| present in query | a                 | b                |
| absent in query  | c                 | d                |


The order of the rows in the table corresponds to the order in the `target_list`. Additionally, one can pass an iterable containing the names of the respective target-items using the `names` parameters. Then, an additional `name` column will be appended to the output.