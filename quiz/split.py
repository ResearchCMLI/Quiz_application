import pandas as pd

# Read CSV
df = pd.read_csv("/home/jayashree/quiz/Inventory.csv", low_memory=False)

# Split into 10k-column chunks
chunk_size = 10000
for i in range(0, df.shape[1], chunk_size):
    chunk = df.iloc[:, i:i+chunk_size]
    chunk.to_csv(f"Inventory_chunk_{i//chunk_size+1}.csv", index=False)
    print(f"Saved Inventory_chunk_{i//chunk_size+1}.csv with columns {i}-{i+chunk.shape[1]-1}")
