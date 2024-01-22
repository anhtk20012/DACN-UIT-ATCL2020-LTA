import os

import torch 
import pandas as pd
import pytorch_lightning as pl
import sastvd as svd
import sastvd.linevd as lvd
from pytorch_lightning.callbacks import ModelCheckpoint

os.environ["SLURM_JOB_NAME"] = "bash"
# samplesz = -1
# run_id = svd.get_run_id()
# sp = svd.get_dir(svd.processed_dir() / f"train_demo_{samplesz}" / run_id)

data = lvd.BigVulDatasetLineVDDataModule(
    batch_size=1024,
    sample=-1,
    methodlevel=False,
    nsampling=True,
    nsampling_hops=2,
    gtype="pdg+raw",
    splits="default",
)

model = lvd.LitGNN(
    hfeat=512,
    embtype="codebert",
    methodlevel=False,
    nsampling=True,
    model="gat2layer",
    loss="ce",
    hdropout=0.3,
    gatdropout=0.2,
    num_heads=4,
    multitask="linemethod",
    stmtweight=1,
    gnntype="gcn",
    scea=0.5,
    lr=1e-4,
)

checkpoint_callback = ModelCheckpoint(monitor="val_loss")

trainer = pl.Trainer(
    accelerator="auto",
    default_root_dir=sp,
    num_sanity_val_steps=0,
    callbacks=[checkpoint_callback],
    max_epochs=130,
)

main_savedir = svd.get_dir(svd.outputs_dir() / "rq_results_methodonly")

trainer.test(model, data, ckpt_path="best")

res = [
    "methodonly",
    "methodonly",
    model.res1vo,
    model.res2mt,
    model.res2f,
    model.res3vo,
    model.res2,
    model.lr,
]
mets = lvd.get_relevant_metrics(res)
res_df = pd.DataFrame.from_records([mets])
res_df.to_csv(str(main_savedir / svd.get_run_id()) + ".csv", index=0)