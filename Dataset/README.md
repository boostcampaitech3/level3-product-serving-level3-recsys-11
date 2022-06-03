# Dataset Used

<br/>

## User_Whiskey_interaction_renamed
---
* Scraped from Whiskybase.com <br/>
* 544117 user interactions
* Pseudonymized using random words

|whiskey| user| rating| price| url|
|-------|-----|-----|-----|-----|
|Macallan 10yo Full Proof 57% 1980 (OB, Giovinetti & Figli)|curves1|99|€ 3320.25|https://www.whiskybase.com/whiskies/whisky/8627/macallan-10-year-old|

<br/>

<br/>

## total_df
---
* Scraped from Whiskybase.com <br/>
* Whiskey normalized features using Whiskey_w_tags_norm<br/>
* Image links and Extra info link in Whiskybase



Whiskey|Meta Critic|STDEV|#|Cost|Class|Super Cluster|cluster|body|sweet|sherry|malt|aperitif|smoky|pungent|fruity|honey|floral|spicy|medicinal|nutty|winey|images|links|
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
Macallan 10yo Full Proof 57% 1980 (OB, Giovine...|9.57|0.24|3|$$$$$+|SingleMalt-like|ABC|A|0.71166|0.611775|1.333333|-1.0|-0.503953|-0.747565|-0.333333|0.333333|1.257656|-0.843274|0.764719|-0.471405|-0.503953|-0.333333|https://static.whiskybase.com/storage/whiskies...|https://www.whiskybase.com/whiskies/whisky/862...
<br/>

<br/>

## Whiskey_w_tags_norm
---
* Scraped from Whisky Analysis <br/>
* Whiskey clusters and tags

Whiskey|Meta Critic|STDEV|#|Cost|Class|Super Cluster|Cluster|Country|Type|body|sweet|sherry|malt|aperitif|smoky|pungent|fruity|honey|floral|spicy|medicinal|nutty|winey|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|"Macallan 10yo Full Proof 57% 1980 (OB, Giovinetti & Figli)"|9.57|0.24|3|$$$$$+|SingleMalt-like|ABC|A|Scotland|Malt|3|3|1|0.0|0|0.0|0|1.0|1.0|0|1.0|0.0|0|0|

<br/>




<br/>

## Reference
---
https://whiskybase.com<br/>
https://github.com/AustinKrause/whiskey-recommender/tree/master/Webscraped%20Data<br/>
https://whiskyanalysis.com/index.php/database/