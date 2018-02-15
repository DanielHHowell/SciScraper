# SciScraper
### --WORK IN PROGRESS--

The goal of this project is to create an efficient means of gathering as much full-text data as possible on a given topic. Legally, this limits the scope of the scraper to a handful of databases that fit this criteria, such as PubMed Central. Pertinent information such as abstracts, conclusions, and figures can then be concatenated into an database. These can then be converted into HTML for viewing, PDF for printing/sending, or perhaps a clean JS presentation for interactive navigation.

The databases used will be those outlined by Unpaywall as open-access: PubMed Central, the DOAJ, Crossref (particulary their license info), DataCite, Google Scholar, and BASE. Currently only utilizing PubMed Central

At the moment, reports can be generated in markdown, and HTML. Working on LaTeX and PDF.

To do:

* Summarizer?
* Curtailing long sections (e.g. authors/abstract)
* Download HTML/PDF feature (email?)
* Interaction?
* Popular searches
* Faster
* Sort by (relevance, date, etc.)
* Remove 'anthology' articles (scrape +2 nResults as buffer?)
* NLTK
* Hoverzoom images
* Article links
* Sidebar nav of studies
* Additional DB's - arXiv, etc.
* Checkbox for reports
* Alert message if not_validate()
* Large-scale analytics with bootstrap cards UI?

Similar projects: 

https://github.com/ContentMine/journal-scrapers (for ContentMine framework)

https://github.com/EFavDB/PubmedCentral_Scraper (in R, only from PubMed)

## Using the Scraper

The scraper takes up to three arguments: a main topic, optional queries, and the maximum number of results to return. It is initialized by running Main.py, and generates the reports as local files in the folder ran.

### Function Documentation

1 - PubMed Central API

The documentation [here](https://www.ncbi.nlm.nih.gov/books/NBK25497/#_chapter2_The_Nine_Eutilities_in_Brief_) provides an overview for how to interact with the PMC database with 9 different utilities. ESearch can be used initially to query the database, then EFetch to retrieve the articles’ information. The scraping from each individual article will be done within the local script using BS4. 

Search terms are [parsed left to right](https://www.nlm.nih.gov/bsd/disted/pubmedtutorial/020_380.html), using capital Boolean operators that are parenthetically encapsulated. For example, to search for the main topic of ‘salmonella’ and one of multiple queries (e.g. eggs or beef) it would be typed “salmonella AND (protein OR amino)”. The user input to the scraper will inherit this method of searching a main topic in additional to optional queries. 
