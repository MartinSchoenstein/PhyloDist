# Profylo

Profylo: an accessible phylogenetic profiling analysis python package : similarity metrics, clustering methods and modules exploration and visualisation

## Installation

All dependencies are described in the pyproject.toml file. As well as the appropriate Python version (3.12.10 recommended) for the conda environment that will host the package.
You can create it with the following commands:
```bash
conda create -n Profylo_env python=3.12
conda activate Profylo_env
```

For now, the package is accessible by downloading the folder on GitHub. Once this is done, in the directory containing the .toml file, you can install the package with the following commands:
```bash
git clone https://github.com/MartinSchoenstein/Profylo.git
cd Profylo
pip install .
```

## Features

Here are some examples of how to use Profylo, using some important functions. The data used and generated files are available on GitHub in /example.

### Generating similarity scores (cotransition scores here) between all profiles in a matrix:
```python
from profylo import Profylo as pro

pro.distance_profiles(x = "/exemple/profiles.csv",  tree = "/exemple/tree.nwk", method = "cotransition", consecutive = False, path = "exemple/cotransition_similarity.csv")
```
Other similarity or distance metrics are available, some with their own customization options, and some without requiring a phylogenetic tree.


### Obtaining functional modules (using the connected components technique here):
```python
from profylo import post_processing as post 

post.graph_modules("exemple/cotransition_similarity.csv", distance = "cotransition", threshold = 0.3, path = "exemple/connected_components.txt")
```
Other clustering methods, some graph-based and non-graph-based, are available.


### Functional characterization of modules:
```python
from profylo import post_processing as post 

post.go_enrichment("exemple/connected_components.txt", gaf = "exemple/gaf.gaf", complete_results = True, path = "GO_enrichment")
```


### Obtaining phylogenetic information relating to modules, the parsimony score is used as a score of atypicality of the modules:
```python
from profylo import post_processing as post 

post.phylogenetic_statistics("exemple/connected_components.txt", profils = "exemple/profiles.csv", path_tree = "exemple/tree.nwk", path = "exemple/phylogenetic_statitstics.csv")
```

## Crédits
Martin Schoenstein

Pauline MermillodYannis Nevers

CSTB - Icube 

April 2025





