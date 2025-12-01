import pandas as pd
import os

# Function to convert train/test.txt into triplets
def create_triplets(input_file, output_file):
    """
    Convert train/test format (<user_id> <item_id_1> <item_id_2> ...) 
    into triplets (user, item, rating) format and save as .csv.
    """
    triplets = []
    with open(input_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            user = parts[0]
            items = parts[1:]
            triplets.extend([(user, item, 1) for item in items])  # Assuming implicit feedback with rating=1

    # Save to CSV
    df = pd.DataFrame(triplets, columns=['user', 'item', 'rating'])
    df.to_csv(output_file, index=False)
    print(f"Converted {input_file} to triplets and saved as {output_file}.")

# Function to process kg.txt into entity-relation form
def process_knowledge_graph(kg_file, entity_file, relation_file):
    """
    Convert kg.txt (user_id rel_id item_id) into entities and relations.
    Entities and relations are saved in separate files.
    """
    entities = set()
    relations = set()
    edges = []

    # Process kg.txt
    with open(kg_file, 'r') as f:
        for line in f:
            head, rel, tail = line.strip().split()
            entities.add(head)
            entities.add(tail)
            relations.add(rel)
            edges.append((head, rel, tail))
    
    # Save entities
    entity_mapping = {entity: idx for idx, entity in enumerate(sorted(entities))}
    with open(entity_file, 'w') as f:
        for entity, idx in entity_mapping.items():
            f.write(f"{entity},{idx}\n")
    print(f"Saved entities to {entity_file}.")

    # Save relations
    relation_mapping = {relation: idx for idx, relation in enumerate(sorted(relations))}
    with open(relation_file, 'w') as f:
        for relation, idx in relation_mapping.items():
            f.write(f"{relation},{idx}\n")
    print(f"Saved relations to {relation_file}.")

    # Map edges using entity/relation indices and save
    edge_list = [(entity_mapping[head], relation_mapping[rel], entity_mapping[tail]) for head, rel, tail in edges]
    edges_df = pd.DataFrame(edge_list, columns=['head', 'relation', 'tail'])
    edges_df.to_csv(kg_file.replace('.txt', '_processed.csv'), index=False)
    print(f"Processed KG edges saved to {kg_file.replace('.txt', '_processed.csv')}.")

# Paths to input dataset
train_file = "train_1.txt"
test_file = "test_1.txt"
kg_file = "kg.txt"

# Paths for output files
output_dir = "processed_dataset"
os.makedirs(output_dir, exist_ok=True)

train_output = os.path.join(output_dir, "train_triplets.csv")
test_output = os.path.join(output_dir, "test_triplets.csv")
entity_file = os.path.join(output_dir, "entities.csv")
relation_file = os.path.join(output_dir, "relations.csv")

# Convert train/test files to triplets
create_triplets(train_file, train_output)
create_triplets(test_file, test_output)

# Process the knowledge graph
process_knowledge_graph(kg_file, entity_file, relation_file)