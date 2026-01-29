
# Boolean mask of duplicates (True for 2nd+ occurrence)

dup_mask = df2.index.duplicated(keep=False)

# Count and preview
dup_count = dup_mask.sum()
print(f"Duplicate index labels: {dup_count}")

# See only duplicated rows
dups_df = df2[dup_mask].sort_index()
dups_df.head()
