$bug = Get-ChildItem -Recurse -Filter "*.bug" | Select-Object -First 1
if ($bug) { Get-Content $bug.FullName } else { Write-Host "Hôm nay không có bug, lạ" }

#!/bin/bash
pip install -r requirements.txt  # hy vọng không conflict

#!/bin/bash
pip install -r requirements.txt  # hy vọng không conflict

