from ray import tune, train
from ray.tune import TuneConfig

def objective(config):
    for i in range(10):
        metric = i + config["alpha"] * config["beta"]
        train.report({"mean_loss": metric})

config = {
    "alpha": tune.grid_search([0.1, 0.2, 0.3]),
    "beta": tune.uniform(1, 2)
}

tuner = tune.Tuner(
    objective,
    param_space=config,
    tune_config=TuneConfig(
        metric="mean_loss",
        mode="min",
        max_concurrent_trials=10,
        num_samples=10,
    )
)

results = tuner.fit()

# best_trial = results.get_best_trial(metric="score", mode="min")
# best_config = best_trial.config
# best_result = best_trial.last_result

# print("Best trial config:", best_config)
# print("Best trial final mean_loss:", best_result["mean_loss"])