import os, sys, re

def get_files(temp, cwd):
   ret = []
   for item in temp:
      if os.path.isdir(cwd+item):
         new_cwd = cwd + item; new_temp = []
         get_temp = os.listdir(cwd+item)
         for file in get_temp:
            get = item + "/" + file
            new_temp.append(get)
         temp.pop(temp.index(item))
         return get_files(temp+new_temp, new_cwd)
      else:
         ret.append(item)
   return ret

try:
   export_dir = sys.argv[1].strip("/\\") + '/'
except:
   export_dir = "mend/templates/"
templates = os.listdir(export_dir)
templates = get_files(templates, export_dir)

for page in templates:
   template = export_dir + page
   with open(template, "r+") as f:
      html = f.read().replace("&quot;", '"')
      static_paths = re.findall(r'(?:(?<=href=")|(?<=src=")|(?<=url\())"?(?:\.\./)?assets/.+?"', html)
      pages = re.findall(r'(?<=href=").+?.html"', html)
      for path in static_paths:
         path = re.sub(r"^\.\./", '', path)
         if path[0] == '"':
            path = path.strip('"')
            html = re.sub(fr'"(\.\./)?{path}"', f"{{{{ url_for('static',filename='{path}') }}}}", html)
         else:
            path = path.strip('"')
            html = re.sub(fr"(\.\./)?{path}", f"{{{{ url_for('static',filename='{path}') }}}}", html)
      for page in pages:
         page = re.sub(r"^\.\./", '', page)
         page = page.strip('"')
         route = re.sub(r'\.html', '', page)
         html = re.sub(fr"(\.\./)?{page}", f"{{{{ url_for('{route}') }}}}", html)

      f.seek(0)
      f.write(html)
      f.truncate()

##with open("LOG.txt", 'a') as L:
##   L.write("\n")
