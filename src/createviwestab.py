from bs4 import BeautifulSoup
import re
import glob
import os
import sys
import shutil

def main(argv):
  elmdatamap = {}
  
  #set html root directory
  #if not argv, html root is current directory.
  htmldir = os.getcwd()
  try:
    if os.path.exists(argv[1]):
      htmldir = argv[1]
  except:
    None
  print("html root directory:" ,htmldir)

  #set target directory and current change.
  iddirs = glob.glob(htmldir + "/id-*")
  if not iddirs:
    print("ID directory not found. Please pass the correct directory as an argument or move the current directory.")
    return -1
  print("id- directory:" ,iddirs[0])
  os.chdir(iddirs[0])
  
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
          try:
            os.mkdir("./elements/bak")
          except:
            None
          shutil.copy2(elmpath, "./elements/bak/")
          with open(elmpath, 'w', encoding='utf-8') as f:
              f.write(str(soup))
              print("Org file bakup to bak directory. and html Rewrite:" , elmpath)

  print("process successfully")
  
if __name__ == '__main__':
    sys.exit(main(sys.argv))