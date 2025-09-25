import kagglehub
import shutil

# Download latest version
path = kagglehub.dataset_download("fukmats/cefrj-wordlist")

target_dir = "dataset"
shutil.copytree(path, target_dir,dirs_exist_ok=True)

print("Path to dataset files:", path)
