import os.path
import zipfile

epub = zipfile.ZipFile('my_ebook.epub', 'w')

# The first file must be named "mimetype"
epub.writestr("mimetype", "application/epub+zip")

# The filenames of the HTML are listed in html_files
html_files = ['coverpage.html', 'foo.html', 'bar.html']

# We need an index file, that lists all other HTML files
# This index file itself is referenced in the META_INF/container.xml
# file
epub.writestr("META-INF/container.xml", '''<container version="1.0"
           xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/Content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>''');

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
    basename = os.path.basename(html)
    manifest += '<item id="file_%s" href="%s" media-type="application/xhtml+xml"/>' % (i+1, basename)
    spine += '<itemref idref="file_%s" />' % (i+1)
    epub.write(html, 'OEBPS/'+basename)

# Finally, write the index
epub.writestr('OEBPS/Content.opf', index_tpl % {
    'manifest' : manifest,
    'spine' : spine,
    'dc' : dc
    })

epub.write('/home/zyqhi/projects/simpleepub/images/cover.jpg', 'OEBPS/images/cover.jpg')

# close the file
epub.close()
