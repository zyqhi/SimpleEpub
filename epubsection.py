#-*-coding:utf-8-*-

# Description :  A simple Epub generator
# Author      :  Yongqiang Zhou
# Date        :  Tue Dec 16 22:19:14 CST 2014
# -:- 他喜欢自己的程度就像你讨厌他一样  -:-
#

class EpubSection:
    def __init__(self, html_file_name):
        self.section_file = html_file_name

    def get_section_file(self):
        return self.section_file

section = EpubSection('hello.html')
print section.get_section_file()        
