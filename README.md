# houdiniResourceManager
Resource Manager for Houdini

It's a Tool which allows you to track,rename and collect external resources.
It allows you to move files arround without loosing their connection within Houdini

## Instalation
 - A. Add the folder containing all the files to your path environement variable
 - B. Comming Soon(More complex but controled package management)

Launch Houdini
 - On the shelf of your choosing, right click -> "New Tool"
 - Go to the "Script" tab
 - Add these few lines
```
import imp
from houdiniResourceManager.ui import main
imp.reload(main)
    
rm = main.resourceManagerUI()
rm.show()
```
