# src/train.py
import pickle
import nfl_data_py as nfl
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from pathlib import Path

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["fp"] = df["fantasy_points_ppr"]
    df["touches"] = df["carries"].fillna(0) + df["targets"].fillna(0)
    df["fp_per_touch"] = df["fp"] / df["touches"].replace(0, np.nan)

    df["roll_touch3"] = (
        df.groupby("player_id")["touches"]
          .transform(lambda s: s.shift().rolling(3, min_periods=1).mean())
    )
    df["roll_fppt3"] = (
        df.groupby("player_id")["fp_per_touch"]
          .transform(lambda s: s.shift().rolling(3, min_periods=1).mean())
    )
    df["team_rb_fp5"] = (
        df.groupby("recent_team")["fp"]
          .transform(lambda s: s.shift().rolling(5, min_periods=1).mean())
    )
    df["opp_rb_fp5"] = (
        df.groupby("opponent_team")["fp"]
          .transform(lambda s: s.shift().rolling(5, min_periods=1).mean())
    )
    df["team_change"] = (
        df.groupby("player_id")["recent_team"]
          .transform(lambda s: (s != s.shift()).astype(int))
    )
    df["games_with_team"] = (
        df.groupby(["player_id", "recent_team"]).cumcount() + 1
    )
    df["games_since"] = (
        df.groupby("player_id")["week"].diff().fillna(1)
    )
    return df

def build_priors(df: pd.DataFrame):
    priors = (
        df.groupby("recent_team")
          .agg(team_touch_mean=("touches", "mean"),
               team_fppt_mean=("fp_per_touch", "mean"))
    )
    return priors, df["touches"].mean(), df["fp_per_touch"].mean()

def main():
    wk = nfl.import_weekly_data(years=list(range(2018, 2025)))
    df = add_features(wk)

    train_df = df[df["season"] < 2024]

    priors_team, global_touch, global_fppt = build_priors(train_df)
    op_features  = ["roll_touch3","team_rb_fp5","opp_rb_fp5","games_with_team","team_change"]
    eff_features = ["roll_fppt3","opp_rb_fp5","games_with_team","team_change"]

    train_op  = train_df.dropna(subset=op_features + ["touches"])
    train_eff = train_df.dropna(subset=eff_features + ["fp_per_touch"])
    op_model = Pipeline([("sc", StandardScaler()), ("lr", Ridge(alpha=1.0))])
    eff_model = Pipeline([("sc", StandardScaler()), ("lr", Ridge(alpha=1.0))])
    op_model.fit(train_op[op_features], train_op["touches"])
    eff_model.fit(train_eff[eff_features], train_eff["fp_per_touch"])

    bundle = {
        "op_model":       op_model,
        "eff_model":      eff_model,
        "priors_team":    priors_team,
        "global_touch":   global_touch,
        "global_fppt":    global_fppt,
        "op_features":    op_features,
        "eff_features":   eff_features,
        "blend_k":        5
    }
    models_dir = Path(__file__).parent.parent / "models"
    models_dir.mkdir(exist_ok=True)
    with open(models_dir / "model_bundle.pkl", "wb") as f:
        pickle.dump(bundle, f)
    print(f"Trained & saved bundle to {models_dir/'model_bundle.pkl'}")

if __name__ == "__main__":
    main()