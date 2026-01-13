import pandas as pd

# Sample input
views = pd.DataFrame({
    'article_id': [1,1,2,2,4,3,3],
    'author_id': [3,3,7,7,7,4,4],
    'viewer_id': [5,6,7,6,1,4,4],
    'view_date': ['2019-08-01','2019-08-02','2019-08-01','2019-08-02','2019-07-22','2019-07-21','2019-07-21']
})


# Step 1: Filter rows where author viewed their own article
self_views = views[views['author_id'] == views['viewer_id']]
print(type(self_views))
# Step 2: Select unique authors
authors = self_views[['author_id']].drop_duplicates().reset_index(drop=True)
print(type(authors))
print(authors)
result = authors.sort_values(by=['author_id']).reset_index(drop=True)
f_result=result[['author_id']].rename(columns={'author_id':'id'})
print(f_result)
# Step 3: Convert to DataFrame with column name 'id' and sort
#result = pd.DataFrame({'id': authors}).sort_values('id').reset_index(drop=True)


def article_views(views: pd.DataFrame) -> pd.DataFrame:
    """docstring for article_views"""
    aut_view = views[views['author_id'] == views['viewer_id']]
    u_aut_view = aut_view[['author_id']].drop_duplicates().reset_index(drop=True)
    s_aut_view = u_aut_view.sort_values(by=['author_id']).reset_index(drop=True)
    final = s_aut_view[['author_id']].rename(columns={'author_id': 'id'})
    return final

