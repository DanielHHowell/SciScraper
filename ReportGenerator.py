import markdown
import codecs
import requests
import pypandoc



def markdown_generator(dictreport, query, nResults):
    #Header information
    title = query
    sep = '----- \n'
    H1 = '> - Showing top ('+str(nResults)+') relevant results from PubMed Central \n'
    H2 = '> - Articles dating from range 2000-2010 \n'
    H3 = '> - Most commonly referenced words in abstract: list here \n'
    header = '# '+title+' (Summary Report) \n'
    with open('Report.md', 'w', encoding="utf-8") as f:
        f.write(header+sep+H1+H2+H3+'\n')
        for PMC in dictreport:
            ref = dictreport[PMC]
            article_title = sep+'\n'+ '### '+ref['Title']+'\n \n'
            authors = '* Author(s): '+', '.join(ref['Authors'])+'\n'
            date = '* Date: '+ref['Date']+'\n'
            DOI = '* DOI: '+ref['DOI']+'\n'
            abstract = '+ Abstract: '+ref['Abstract']+'\n'
            f.write(article_title+authors+date+DOI+'\n'+abstract)


def markdown_generator_with_images(dictreport, query, nResults):
    #Header information
    title = query
    sep = '----- \n'
    H1 = '> - Showing top ('+str(nResults)+') most relevant results from PubMed Central \n'
    H2 = '> - Articles dating from range 2000-2010 \n'
    H3 = '> - Most commonly referenced words in abstract: list here \n'
    header = '# '+title+' (Summary Report) \n'
    with open('Report.md', 'w', encoding="utf-8") as f:
        f.write(header+sep+H1+H2+H3+'\n')
        for PMC in dictreport:
            ref = dictreport[PMC]
            article_title = sep+'\n'+ '### '+ref['Title']+'\n \n'
            authors = '* Author(s): '+', '.join(ref['Authors'])+'\n'
            date = '* Date: '+ref['Date']+'\n'
            DOI = '* DOI: '+ref['DOI']+'\n'
            abstract = '+ Abstract: '+ref['Abstract']+'\n'
            images = '\n'.join(['![alt text]('+i+')' for i in ref['Images']])+'\n'
            f.write(article_title+authors+date+DOI+'\n'+abstract+images)


def htmltest():
    input_file = codecs.open("Report.md", mode="r", encoding="utf-8")
    text = input_file.read()
    html = markdown.markdown(text)
    output_file = codecs.open("Report.html", "w",
                              encoding="utf-8",
                              errors="xmlcharrefreplace")
    output_file.write(html)

def pdftest():
    output = pypandoc.convert_file('Report.md', 'pdf', outputfile="Report.pdf")
