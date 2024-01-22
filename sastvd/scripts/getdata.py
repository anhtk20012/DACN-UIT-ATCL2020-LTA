import os

import pandas as pd
import pytorch_lightning as pl
import sastvd as svd
import sastvd.linevd as lvd

os.environ["SLURM_JOB_NAME"] = "bash"

config = {
    "gnntype": "gat",
    "hdropout": 0.3,
    "gatdropout": 0.2,
    "modeltype": "gat2layer",
}
samplesz=-1
run_id = svd.get_run_id()
sp = svd.get_dir(svd.processed_dir() / f"raytune_methodlevel_{samplesz}" / run_id)

data = lvd.BigVulDatasetLineVDDataModule(
    batch_size=32,
    sample=samplesz,
    methodlevel=True,
    nsampling=False,
    nsampling_hops=2,
    gtype="pdg+raw",
    splits="default",
    feat="glove",
)

model = lvd.LitGNN(
    methodlevel=True,
    nsampling=False,
    model=config["modeltype"],
    embtype="glove",
    loss="ce",
    hdropout=config["hdropout"],
    gatdropout=config["gatdropout"],
    num_heads=4,
    multitask="line",
    stmtweight=1,
    gnntype=config["gnntype"],
    lr=1e-4,
)

trainer = pl.Trainer(
    gpus=1,
    auto_lr_find=False,
    default_root_dir=sp,
    num_sanity_val_steps=3,
    max_epochs=130,
)

trainer.fit(model, data)