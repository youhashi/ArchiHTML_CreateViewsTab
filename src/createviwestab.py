from bs4 import BeautifulSoup
import re
import glob
import os

elmdatamap = {}

#exsample for windows
#htmldir = "C:\\archihtml\\"
htmldir = "D:\\Development\\Repository\\Task_and_CMDB_Test\\archihtml\\"
targetdir = "id-5226cdc5cb724642a8481fdad0b8154b"
os.chdir(htmldir + targetdir)

#Get all element filepath. dic key is filepath
elmfiles = glob.glob("./elements/id-*.html")
for elmfilepath in elmfiles:
    elmdatamap[elmfilepath.replace("\\", "/")] = []


#create dic values.
#dic value is view filepath list.
viewfiles = glob.glob("./views/*")
for viewfilepath in viewfiles:

    viewdatamap = {}

    with open(viewfilepath, encoding='utf-8') as f:
        html = f.read()

        soup = BeautifulSoup(html, 'html.parser')

        viewname = soup.find("title").text
        viewfilepath = "." + viewfilepath


        elmpathlist = []
        for elm in soup.find_all("a",class_=re.compile("^i18n-elementtype.*")):
            elmpath = elm.get("href")[1:]
            elmdatamap[elmpath].append([viewfilepath, viewname])

#create view filepath in elements tab and do rewrite the elements html files.
for elmpath in elmdatamap:
    soup = ""
    with open(elmpath, 'r', encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')

        if str(soup.find("div", id="views")) == 'None':
            #create Nav tabs
            li = soup.new_tag('li', role='presentation')
            a = soup.new_tag('a', href="#views")
            a.attrs['aria-controls'] ="views"
            a.attrs['role'] = "tab"
            a.attrs['data-toggle'] = "tab"
            a.attrs['class'] = "i18n-views"
            li.append(a)
            soup.find("ul", class_="nav nav-tabs").append(li)

            #create view-tab table
            div = soup.new_tag('div',id='views')
            div.attrs['role'] = "tabpanel"
            div.attrs['class'] = "tab-pane"
            table = soup.new_tag('table', class_="table table-striped table-hover table-condensed")
            thead = soup.new_tag('thead')
            for viewdata in elmdatamap[elmpath]:
                a = soup.new_tag('a', href=viewdata[0].replace("\\","/") )
                a.attrs['target'] = "view"
                a.string = viewdata[1]
                tr = soup.new_tag('tr')
                td = soup.new_tag('td')
                td.append(a)
                tr.append(td)
                thead.append(tr)

            table.append(thead)
            div.append(table)
            soup.find("div", class_="tab-content").append(div)
        else:
            soup = ""

    #rewrite html files.
    if soup != "":
        with open(elmpath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            print("Rewrite:" , elmpath)
