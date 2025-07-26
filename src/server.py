# src/server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import nfl_data_py as nfl
import pandas as pd

from src.model_utils import load_bundle
from src.train import add_features 

app = FastAPI(title="Fantasy‑Points Predictor")
bundle = load_bundle()

op_model = bundle["op_model"]
eff_model = bundle["eff_model"]
priors_team = bundle["priors_team"]
global_touch = bundle["global_touch"]
global_fppt = bundle["global_fppt"]
op_features = bundle["op_features"]
eff_features = bundle["eff_features"]
blend_k = bundle["blend_k"]

class PredictReq(BaseModel):
    player_id: int
    season: int
    week: int

class PredictResp(BaseModel):
    player_id: int
    season: int
    week: int
    expected_points: float

@app.post("/predict", response_model=PredictResp)
def predict(req: PredictReq):
    df = nfl.import_weekly_data(years=[req.season])
    df = df[(df.player_id == req.player_id) & 
            (df.season == req.season)   & 
            (df.week == req.week)]
    if df.empty:
        raise HTTPException(404, "No data for that player/season/week")
    row = add_features(df).iloc[0]

    # Check if we have all required features
    missing_op = [f for f in op_features if pd.isna(row[f])]
    missing_eff = [f for f in eff_features if pd.isna(row[f])]
    
    if missing_op or missing_eff:
        raise HTTPException(400, f"Missing required features: op={missing_op}, eff={missing_eff}")
    
    X_op  = row[op_features].values.reshape(1, -1)
    X_eff = row[eff_features].values.reshape(1, -1)

    touch_hat = float(op_model.predict(X_op))
    fppt_hat  = float(eff_model.predict(X_eff))

    n = row["games_with_team"]
    team = row["recent_team"]
    prior_touches = (priors_team
                     .get("team_touch_mean")
                     .loc[team]
                     if team in priors_team.index
                     else global_touch)
    prior_fppt = (priors_team
                  .get("team_fppt_mean")
                  .loc[team]
                  if team in priors_team.index
                  else global_fppt)

    w = n / (n + blend_k)
    touch_blend = w * touch_hat + (1 - w) * prior_touches
    fppt_blend = w * fppt_hat + (1 - w) * prior_fppt

    pred = touch_blend * fppt_blend

    return PredictResp(
        player_id=req.player_id,
        season=req.season,
        week=req.week,
        expected_points=pred
    )