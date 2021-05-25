# %%
"""

Copyright 2018 Peter C Kroon

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

In accordance with the license, file modications are described below:

The original pysmiles logic has been used such that a string of any 
uppercase letters, A-Z, can be used to create a networkx opbject.
Tokenisation, aromaticity handling, bond order handling and stereo
handling functionalities have been removed. 

The original file is available at

    https://github.com/pckroon/pysmiles/blob/master/pysmiles/read_smiles.py

"""

from typing import *
import networkx as nx
import re
import matplotlib.pyplot as plt


def read_smiles(smiles) -> nx.Graph:
    G = nx.Graph()
    anchor = None
    idx = 0
    default_bond = 1
    next_bond = None
    branches = []
    ring_nums = {}
    for char in list(smiles):
        if re.match("[A-Z]", char):
            G.add_node(idx, **{"sub": char, "processed": False})
            if anchor is not None:
                if next_bond is None:
                    next_bond = default_bond
                if next_bond:
                    G.add_edge(anchor, idx, order=next_bond)
                next_bond = None
            anchor = idx
            idx += 1
        elif char == "(":
            branches.append(anchor)
        elif char == ")":
            anchor = branches.pop()
        elif re.match("[1-9]", char):
            num = int(char)
            if num in ring_nums:
                jdx, order = ring_nums[num]
                if next_bond is None and order is None:
                    next_bond = default_bond
                elif order is None:  # Note that the check is needed,
                    next_bond = next_bond  # But this could be pass.
                elif next_bond is None:
                    next_bond = order
                elif next_bond != order:  # Both are not None
                    raise ValueError(
                        f"Conflicting bond orders for ring " "between indices {num}"
                    )
                # idx is the index of the *next* atom we're adding. So: -1.
                if G.has_edge(idx - 1, jdx):
                    raise ValueError(
                        f"Edge specified by marker {num} already " "exists"
                    )
                if idx - 1 == jdx:
                    raise ValueError(
                        "Marker {} specifies a bond between an "
                        "atom and itself".format(num)
                    )
                if next_bond:
                    G.add_edge(idx - 1, jdx, order=next_bond)
                next_bond = None
                del ring_nums[num]
            else:
                if idx == 0:
                    raise ValueError(f"Can't have a marker ({num}) before an atom" "")
                # idx is the index of the *next* atom we're adding. So: -1.
                ring_nums[num] = (idx - 1, next_bond)
                next_bond = None
    if ring_nums:
        raise KeyError(f"Unmatched ring indices {list(ring_nums.keys())}")
    return G


# %%
