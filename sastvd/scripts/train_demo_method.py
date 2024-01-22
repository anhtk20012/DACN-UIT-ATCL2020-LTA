import os

import torch 

import pytorch_lightning as pl
import sastvd as svd
import sastvd.linevd as lvd
from pytorch_lightning.callbacks import ModelCheckpoint

os.environ["SLURM_JOB_NAME"] = "bash"

samplesz = -1
run_id = "203" #svd.get_run_id()
sp = svd.get_dir(svd.processed_dir() / f"train_demo_{samplesz}" / run_id)

model = lvd.LitGNN(
    hfeat=512,
    embtype="glove",
    methodlevel=False,
    nsampling=True,
    model="mlponly",
    loss="ce",
    hdropout=0.2,
    gatdropout=0.15,
    num_heads=4,
    multitask="line",
    stmtweight=1,
    gnntype="gat",
    scea=0.4,
    lr=1e-4,
)

# Load data
data = lvd.BigVulDatasetLineVDDataModule(
    batch_size=1024,
    sample=samplesz,
    methodlevel=False,
    nsampling=True,
    nsampling_hops=2,
    gtype="pdg+raw",
    splits="default",
)

print(data)
print(model)

# checkpoint_callback = ModelCheckpoint(monitor="val_loss")

# trainer = pl.Trainer(
#     accelerator="auto",
#     default_root_dir=sp,
#     num_sanity_val_steps=0,
#     callbacks=[checkpoint_callback],
#     max_epochs=130,
# )

# trainer.fit(model, data)
