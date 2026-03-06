# Introduction & Motivation

Quick Note: I will use the term *metrics* a lot. This simply refers to any non-traditional counting stat - anything from Average exit velocity to fastball IVB to SwStr%. 

## Approach: ML-Based Rate Prediction
The idea behind this project is simple; utilize machine learning to decipher the relationships between metrics and fantasy baseball performance. Traditional ESPN fantasy scoring relies heavily on basic counting stats, and although these counting stats hold a lot of randomness, there is still a lot of information to be extracted. Here I set up a model to predict rate agnostic fantasy points (per AB/IP) using the *preceding* seasons metrics. So using metrics + advanced stats from 2025, the model will predict fantasy performance for 2026. I utilize projections for AB and IP from Fangraphs (as they are far more reliable than any sort of projections I could create) to construct season-long fantasy totals. I also remove pitcher wins, losses, saves and holds from the machine learning feature set, as I felt they are too uncorrelated with the true performance of a pitcher. These stats are also taken from Fangraphs projections when aggregating. 

The goal is to create a powerful yet interpretable model that can guide projections - not necessarily the gospel. The use of SHAP plots are critical here to understand why predictions are driven a certain way, along with possibly hinting at an area to dig deeper on a certain player. The balance between predictive power and interpretability is something you will notice frequently drives decisions here. 

## Scoring System (ESPN default points)
- Batters: TB + R + RBI + BB + SB - K
- Pitchers (Skill): 3×IP + K - BB - H - 2×ER
- Pitchers (Team): W/L/SV/HLD from external projections

