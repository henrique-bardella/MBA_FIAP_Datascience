from google_play_scraper import Sort, reviews_all, reviews, app
import pandas as pd
import numpy as np

# Conexao com a página 
# https://play.google.com/store/apps/details?id=br.com.petz&hl=pt_BR&gl=US&showAllReviews=true

result = reviews_all(
    'br.com.petz',
    sleep_milliseconds = 0,
    lang = 'pt',
    sort=Sort.NEWEST,
    count = 500,
    filter_score_with = None
)
# scraped = np.array(result)
# print(scraped)

# Dataframe
scrapeddata = pd.DataFrame(np.array(result),columns=['review'])

scrapeddata = scrapeddata.join(pd.DataFrame(scrapeddata.pop('review').tolist()))

scrapeddata.head()

# len(scrapeddata.index)

# Extração
scrapeddata.to_excel('Petz_google_Play_Store.xlsx', index=False)