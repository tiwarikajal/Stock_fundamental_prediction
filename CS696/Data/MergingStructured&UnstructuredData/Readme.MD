1. Run Merge_Emb_to_pickle.py to convert the torch format embeddings to pickle files for merging.
2. Run Merge_Emb_Time.py to convert the pickle embeddings to format with 't-1' and 't-2' column values.
3. Run Merge_struc_unstruc.py to merge structured and unstructured data (wherever we dont find any fundamental value, we use a placeholder "structuredDataNotFound')
4. Run Final_Merge.py to obtain combined dataset with both structured and embeddings data.