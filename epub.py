#-*-coding:utf-8-*-

# Description :  A simple Epub generator
# Author      :  Yongqiang Zhou
# Date        :  Sat Dec 13 21:03:37 CST 2014
# -:- 为另外一个人改变自己真是很残酷的事情啊  -:-

#C-u M-! insert shell command output to emacs buffer

import os.path
from zipfile import ZipFile
from epubsection import EpubSection

class EpubGen(ZipFile):
    def __init__(self, name):
        ZipFile.__init__(self, name, 'w')
        # write the first file minetype
        self.write_mimetype()
        self.write_index_file()
    
    # The first file must be named "mimetype"
    def write_mimetype(self):
        self.writestr("mimetype", "application/epub+zip")
    
    # Epub need a index file that lists all other HTML files
    # This index file itself is referenced in the META_INF/container.xml
    # file
    def write_index_file(self):
        self.writestr("META-INF/container.xml",
                      '''<container version="1.0"
                      xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
                      <rootfiles>
                      <rootfile full-path="OEBPS/Content.opf" media-type="application/oebps-package+xml"/>
                      </rootfiles>
                      </container>''')



epub = EpubGen('my_ebook.epub')

html_files = []
html_files.append(EpubSection('coverpage.html'))
html_files.append(EpubSection('foo.html'))
html_files.append(EpubSection('bar.html'))

# The filenames of the HTML are listed in html_files
#html_files = [, 'foo.html', 'bar.html']

# The index file is another XML file, living per convention
# in OEBPS/Content.xml
index_tpl = '''<package version="2.0"
  xmlns="http://www.idpf.org/2007/opf">
  <metadata>
    %(dc)s
  </metadata>
  <manifest>
    %(manifest)s
  </manifest>
  <spine toc="ncx">
    %(spine)s
  </spine>
</package>'''

dc = "<dc:title>Hello world</dc:title>"
manifest = ""
spine = ""

# Write each HTML file to the ebook, collect information for the index
for i, html in enumerate(html_files):
    basename = os.path.basename(html.get_section_file())
    manifest += '<item id="file_%s" href="%s" media-type="application/xhtml+xml"/>\n    ' % (i+1, basename)
    spine += '<itemref idref="file_%s" />\n    ' % (i+1)
    epub.write(html.get_section_file(), 'OEBPS/'+basename)

# Finally, write the index
epub.writestr('OEBPS/Content.opf', index_tpl % {
    'manifest' : manifest,
    'spine' : spine,
    'dc' : dc
    })

# Add cover images
epub.write('images/cover.jpg', 'OEBPS/images/cover.jpg')

# close the file
epub.close()
