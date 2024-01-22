import sastvd.linevd as lvd
import pytorch_lightning as pl
import torch

# data = lvd.BigVulDatasetLineVDDataModule(
#     batch_size=1024,
#     sample=-1,
#     methodlevel=False,
#     nsampling=True,
#     nsampling_hops=2,
#     gtype="pdg+raw",
#     splits="default",
# )

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
    gnntype="gat",
    scea=0.5,
    lr=1e-4,
)
