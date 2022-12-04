# ArchiHTML_CreateViewsTab

Archi adds the views tab to the elements in the output html file and overwrites the html file.
 
# DEMO
 
 Does not written it yet.

# Features
 
 Archi is a great software for EA modeling. However, it only outputs to html files a portion of what the application can do.
If an element is drawn in multiple Views, the Analysis tab of the application plays an important role in knowing which View it is drawn in.
This program will add a Views tab to the element's tab in the output html file and add a hyperlink to the view it is drawing in, overwriting the View tab.
 
# Requirement
 
* python 3.x

# Installation
 
* Recomend

Edit model.js file :[Archi Root directory]\plugins\com.archimatetool.reports_4.10.0.202209150946\templates\html\js\model.js

before(default)
```javascript
    west: {
			size: 350,
			spacing_open: 8
		},
```

after
```javascript
    west: {
			size: 380,
			spacing_open: 8
		},
```
# Usage
 
```powershell
git clone https://github.com/youhashi/ArchiHTML_CreateViewsTab.git
cd ArchiHTML_CreateViewsTab
python ./createviewstab.py [targethtmldirectory]
```
## Exsample
```powershell
> python ./createviewstab.py C:\archHTMLReportDirectory\archihtml
```

 
# Note
 
 
# Author
 
* name:yosuke hashimoto
 
# License
 
Inherits the license agreement of Archi.