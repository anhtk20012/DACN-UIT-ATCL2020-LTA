import subprocess
from datetime import datetime

def gitsha():
    """Get current git commit sha for reproducibility."""
    return (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        .strip()
        .decode()
    )
    
def gitmessage():
    """Get current git commit sha for reproducibility."""
    m = subprocess.check_output(["git", "log", "-1", "--format=%s"]).strip().decode()
    return "_".join(m.lower().split())

def get_run_id(args=None):
    """Generate run ID."""
    if not args:
        ID = datetime.now().strftime("%Y%m%d%H%M_{}".format(gitsha()))
        return ID + "_" + gitmessage()
    ID = datetime.now().strftime(
        "%Y%m%d%H%M_{}_{}".format(
            gitsha(), "_".join([f"{v}" for _, v in vars(args).items()])
        )
    )
    return ID

print(get_run_id())
