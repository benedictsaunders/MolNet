# MolNet
A python module that creates dendrimer geometries from inputted SMILES building blocks.

A network is built using a core, vertices, edges, and terminator species, defined with SMILES.

The user will be able to input building blocks as a dictionary, for example.

```python
building_blocks = {
              'A': 'Brc1nc(Br)nc(Br)n1',
              'B': 'Brc1cc2CCc3cc(Br)cc4ccc(c1)c2c34'
              'C': 'BrCC(O)(O)CBr'
              'D': 'BrCC(=O)O'
}
```

Then, the components of the netork can be defined with SMILES-like nomenclature, using the members of the dictionary:

```python
core = 'ACA'
vertices = 'A',
edge = 'AB(CB1)CA1'
terminator = 'D'
```

More to come!

To-do:

- [x] NetworkX builder
- [x] Modified smiles reader
- [ ] Join components to form building blocks
- [ ] Join blocks to form molecular network
