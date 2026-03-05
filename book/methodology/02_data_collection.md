# Data Collection & Preparation

## Data Sources
Data is compiled using pybaseball (or manual export for fangraphs projections) from the following sources:
- FanGraphs (batting/pitching stats, Statcast metrics)
- Baseball Savant (Stuff+, expected stats)
- External projections (Steamer, BatX, OOPSY)

Data ranges from 2015-2025. 


## Fantasy Point Calculation

Once all data is compiled fantasy points are calculated using the previously specified scoring settings and converted to a rate basis (per at bat for hitters, per inning pitched for pitchers). Once again, pitcher wins, losses, saves and holds are omitted from the actual model due to the randomness and reliance on other factors such as team performance. 


## Data Cleaning
Minimum PA/IP thresholds are as follows:
Training data:                                                                                                                                                                            
- Batters: 100 PA minimum                                                                                                                                                                   
- Pitchers: 20 IP minimum                                                                                                                                                                   
                                                                                                                                                                                                            
Prediction data thresholds (for 2026):
- Batters: 50 PA minimum
- Pitchers: 10 IP minimum


Players in their rookie season are dropped from the training set - as lag (prior season) features along with trend features (eg. 2024 xwOBA - 2025 xwOBA) are utilized in the model. 
