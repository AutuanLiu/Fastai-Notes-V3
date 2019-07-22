# Algorithm

## DeepWalk

1. Perform **random walks** on nodes in a graph to generate **node sequences**
2. Run **skip-gram** to learn the **embedding of each node** based on the node sequences generated in step 1

Message passing is the essence of GNN which describes how node embeddings are learned