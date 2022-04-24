### Tasks
1. Creating a new Scrapy project
2. Writing a spider to crawl a site and extract data
3. Exporting the scraped data using the command line
4. Changing spider to recursively follow links
5. Using spider arguments

### Command line
Enter a directory where you’d like to store your code and run:

    scrapy startproject tutorial

To put our spider to work, go to the project’s top level directory and run:
    
    scrapy crawl quotes

using the Scrapy shell. Run:

    scrapy shell 'https://quotes.toscrape.com/page/1/'

The simplest way to store the scraped data is by using Feed exports:

    scrapy crawl quotes -O quotes.json

### The way of extract data
    >>> response.css('title')
    [<Selector xpath='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]
    >>> response.css('title::text').getall()
    ['Quotes to Scrape']
    >>> response.css('title').getall()
    ['<title>Quotes to Scrape</title>']
    >>> response.css('title::text').get()
    'Quotes to Scrape'
    >>> response.css('title::text')[0].get()
    'Quotes to Scrape'
    >>> response.css('noelement')[0].get()
    Traceback (most recent call last):
    ...
    IndexError: list index out of range
    >>> response.css('title::text').re(r'Quotes.*')
    ['Quotes to Scrape']
    >>> response.css('title::text').re(r'Q\w+')
    ['Quotes']
    >>> response.css('title::text').re(r'(\w+) to (\w+)')
    ['Quotes', 'Scrape']

### A shortcut for creating Requests
normal creating Request objects:
```python
next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
```

a shortcut for creating Request objects,you can use `response.follow`:
```pycon
next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
```

You can also pass a selector to `response.follow` instead of a string; this selector should extract necessary attributes:
```python
for href in response.css('ul.pager a::attr(href)'):
    yield response.follow(href, callback=self.parse)
```

For `<a>` elements there is a shortcut: `response.follow` uses their href attribute automatically. So the code can be shortened further:
```python
for a in response.css('ul.pager a'):
    yield response.follow(a, callback=self.parse)
```

To create multiple requests from an iterable, you can use `response.follow_all` instead:
```python
anchors = response.css('ul.pager a')
yield from response.follow_all(anchors, callback=self.parse)
```

or, shortening it further:
```python
yield from response.follow_all(css='ul.pager a', callback=self.parse)
```

### Zyte Scrapy Cloud


