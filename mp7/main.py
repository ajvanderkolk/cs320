from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LogisticRegression
import pandas as pd

class UserPredictor():
    def __init__(self):
        self.pipe = Pipeline([
                ("poly", PolynomialFeatures(1)), # degree 1 does nothing
                ("std", StandardScaler()),
                ("lr", LogisticRegression()),
            ])
        # self.X = ["age", "past_purchase_amt", "gold", "bronze"]
        self.X = ["age","past_purchase_amt","gold","bronze","seconds","num_visits","unique_page_visits","url","url2"]
        self.y = "y"
        return
    
    
    # fit method
    def fit(self, train_users, train_logs, train_y):
        train_df = self._clean(train_users, train_logs, train_y)
        self.pipe.fit(train_df[self.X], train_df[self.y])        
        
        return # train_df
    
    # predict method
    def predict(self, test_users, test_logs):
        test_users = self._reshape(test_users, test_logs)
        predicted_y = self.pipe.predict(test_users[self.X])
        
        return predicted_y
    
    def score(self, test_users, test_logs):
        test_users = self._reshape(test_users, test_logs)
        score = self.pipe.score(test_users[self.X], test_users[self.y])
        
        return score
    
    
    def _clean(self, train_users, train_logs, train_y):
        
        # transform users
        train_users.loc[train_users['badge'] == "gold", "gold"] = 1
        train_users.loc[train_users['badge'] == "silver", "silver"] = 1
        train_users.loc[train_users['badge'] == "bronze", "bronze"] = 1
        train_users.fillna(value=0, inplace=True)
        train_y["y"] = train_y["y"].astype("int")
        
        # join columns
        train_df = train_y.join(train_users, on="user_id", how="left", rsuffix='_other')
        train_df.drop(["badge", "user_id_other"], axis=1, inplace=True)
        
        # transform logs
        new_logs = train_logs.groupby("user_id")["seconds"].agg("sum").reset_index()
        new_logs["num_visits"] = train_logs.groupby("user_id")["date"].agg("count").reset_index()["date"]
        new_logs["unique_page_visits"] = train_logs.groupby(["user_id"]).agg({"url": pd.Series.nunique}).reset_index()["url"]
        
        tmp = train_logs.groupby(["user_id", "url"]).agg({"date": pd.Series.nunique}).reset_index()
        tmp = tmp.loc[tmp['date'] > 1]
        tmp = tmp.groupby("user_id").agg({"url": "count"}).reset_index()
        tmp["url2"] = tmp["url"] ** 2
        tmp.set_index("user_id", inplace=True)
        
        new_logs = new_logs.join(tmp, on="user_id", how="left")
        new_logs.fillna(value=0, inplace=True)
        new_logs.set_index("user_id", inplace=True)
        
        # join columns
        train_df = train_df.join(new_logs, on="user_id", how="left")
        train_df.fillna(value=0, inplace=True)
        
        return train_df
    
    def _reshape(self, test_users, test_logs):
        
        # transform users
        test_users.loc[test_users['badge'] == "gold", "gold"] = 1
        test_users.loc[test_users['badge'] == "silver", "silver"] = 1
        test_users.loc[test_users['badge'] == "bronze", "bronze"] = 1
        test_users.fillna(value=0, inplace=True)
        
        # transform logs
        new_logs = test_logs.groupby("user_id")["seconds"].agg("sum").reset_index()
        new_logs["num_visits"] = test_logs.groupby("user_id")["date"].agg("count").reset_index()["date"]
        new_logs["unique_page_visits"] = test_logs.groupby(["user_id"]).agg({"url": pd.Series.nunique}).reset_index()["url"]
        
        tmp = test_logs.groupby(["user_id", "url"]).agg({"date": pd.Series.nunique}).reset_index()
        tmp = tmp.loc[tmp['date'] > 1]
        tmp = tmp.groupby("user_id").agg({"url": "count"}).reset_index()
        tmp["url2"] = tmp["url"] ** 2
        tmp.set_index("user_id", inplace=True)
        
        new_logs = new_logs.join(tmp, on="user_id", how="left")
        new_logs.fillna(value=0, inplace=True)
        new_logs.set_index("user_id", inplace=True)
        
        # join columns
        test_users = test_users.join(new_logs, on="user_id", how="left")
        test_users.drop("badge", axis=1, inplace=True)
        test_users.fillna(value=0, inplace=True)
        
        return test_users