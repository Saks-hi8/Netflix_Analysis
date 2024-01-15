#!/usr/bin/env python
# coding: utf-8

# # Netflix_Dataset_Analysis

# Task 1 : What is the most popular realase year for movies on Netflix
# 
# Task 2 : What year did netflix add the most content to its platform ?
# 
# Task 3 : Independent of year, what is the most popular month to add new content?
# 
# Task 4 : What is the movie with longest title
# 
# Task 5 : Most frequent actor/actoress in Netflix
# 
# Task 6 : How many movies are there compared to TV shows?
# 
# Task 7 : Which countries contribute the most content to Netflix?
# 
# Task 8 :  Which genres are more prevalent on Netflix?
# 

# In[173]:


#Import necessary libararies 
import pandas as pd
import matplotlib.pyplot  as plt


# ## Task 1 : What is the most popular realase year for movies on Netflix

# In[14]:


df = pd.read_csv('/Users/sakshichavan/Downloads/netflix_titles.csv')


# In[17]:


movie_df = df[df['type'] == 'Movie']


# In[26]:


movie_df['count'] = 1 
release_yr_summed = movie_df.groupby(['release_year']).sum().reset_index()[['release_year','count']]


# In[27]:


release_yr_summed.sort_values(['count'], ascending = False)


# ## Task 2 : What year did netflix add the most content to its platform ?

# In[34]:


df['new_date'] = pd.to_datetime(df['date_added'])

df['date_added_yr'] = df['new_date'].dt.year

df.head(3)


# In[36]:


df['count'] = 1 
date_added_yr_summed = df.groupby(['date_added_yr']).sum().reset_index()[['date_added_yr','count']]


# In[38]:


date_added_yr_summed.sort_values(['count'], ascending = False)


# ## Task 3 : Independent of year, what is the most popular month to add new content?

# In[47]:


df['date_month'] = df['new_date'].dt.month
df['date_month_str'] = df['new_date'].dt.strftime('%b')
df = df.drop(['date_month', 'date_month_str'], axis=1)


# In[46]:


df.head()


# In[48]:


date_added_Month_summed = df.groupby(['month']).sum().reset_index()[['month','count']]


# In[49]:


date_added_Month_summed.sort_values(['count'], ascending = False)


# In[98]:


plt.figure(figsize=(12, 6))
plt.bar(date_added_Month_summed['month'], date_added_Month_summed['count'], color='skyblue')
plt.title('Sum of Counts by Month')
plt.xlabel('Month')
plt.ylabel('Sum of Counts')
plt.show()


# ## Task 4 : What is the movie with longest title?

# In[51]:


df.head()
movie_df = df[df['type'] == 'Movie']


# In[52]:


movie_df['title_len'] = [len(title) for title in movie_df['title']]


# In[54]:


top_title_len = movie_df.sort_values(['title_len'], ascending = False)
top_title_len.iloc[0]['title']


# ## Task 5 : Most frequent actor/actoress in Netflix

# In[55]:


title_cast_df = df[['title', 'cast']]


# In[179]:


cast_name_counter = {}

for index, row in title_cast_df.iterrows():
    movie_cast = row['cast']
    
    if isinstance(movie_cast, str):
        movie_cast_split = movie_cast.split(',')
        movie_cast_stripped = [name.strip().lower() for name in movie_cast_split]
        for name in movie_cast_stripped:
            cast_name_counter[name] = cast_name_counter.get(name, 0) + 1
    
sorted_cast_names = dict(sorted(cast_name_counter.items(), key=lambda item: item[1], reverse = True))

top_10_names = list(sorted_cast_names.items())[:10]
for name, count in top_10_names:
    print(f'{name}: {count}')


# ## Task 6 : How many movies are there compared to TV shows?

# In[80]:


monthly_type_distribution = df.groupby(['month', 'type']).size().unstack(fill_value=0)
monthly_type_distribution 


# In[122]:


monthly_type_distribution.plot(kind='bar', figsize=(12, 6), width=0.4, position=1)

plt.title('Monthly Distribution of Content Types on Netflix')
plt.xlabel('Month')
plt.ylabel('Number of Shows/Movies')
plt.legend(title='Content Type', loc='upper right')
plt.show()


# ## Task 7 : Which countries contribute the most content to Netflix?

# In[128]:


df_cleaned = df.dropna(subset=['country'])
country_counts = df_cleaned['country'].value_counts()

country_counts.head(10)


# In[129]:


plt.figure(figsize=(12, 6))
top_countries.plot(kind='bar')
plt.title('Top 10 Countries Contributing Content to Netflix')
plt.xlabel('Country')
plt.ylabel('Number of Titles')
plt.show()


# ## Task 8 :  Which genres are more prevalent on Netflix?

# In[138]:


df_cleaned = df.dropna(subset=['listed_in'])


df_cleaned['genres'] = df_cleaned['listed_in'].str.split(', ')
all_genres = [genre for sublist in df_cleaned['genres'].dropna() for genre in sublist]

genre_counts = pd.Series(all_genres).value_counts()
genre_counts.head(10)


# In[168]:


plt.figure(figsize=(6, 6))
top_genres.plot(kind='pie', autopct='%1.1f%%', startangle=90, fontsize=8, legend = None)
plt.title('Top 10 Prevalent Genres on Netflix')
plt.ylabel('Genre')
plt.show()

