import numpy as np
import pandas as pd
import umap

def save_umap_dataset(source_path: str) -> None:
    features_df: pd.DataFrame = pd.read_pickle(source_path)    
    
    # Get the feature vectors
    feature_vectors: np.ndarray = features_df['data'].to_numpy()

    reducer = umap.UMAP(
        n_components=100,
    )
    # Get the embeddings
    embeddings: np.ndarray = reducer.fit_transform(feature_vectors)

    features_df['data'] = embeddings.tolist()

    # Save the dataset
    features_df.to_pickle('umap_dataset.pkl')

def load_umap_dataset(source_path: str) -> pd.DataFrame:
    # Load the features
    part: pd.DataFrame = pd.read_pickle(source_path)
    return part 