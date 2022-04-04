from requests_html import HTMLSession

class Scraper():
  def scrapeMultiple(self):
    url = 'https://www.theguardian.com/uk';

    s = HTMLSession()
    r = s.get(url)

    qlist = []
    articles = r.html.find('.fc-item__container')

    for article in articles:
      articleLink = article.find('a.js-headline-text', first=True)
      hrefLink = articleLink.xpath('//a', first=True)
      thumbnailLink = article.find('.fc-item__image-container > picture > img', first=True)
      description = article.find('.fc-item__standfirst', first=True)

      if (thumbnailLink and description):
        imageThumbnailLink = thumbnailLink.xpath('//img', first=True)
        item = {
          'title': article.find('.fc-item__title', first=True).text.strip(),
          'url': hrefLink.attrs['href'],
          'thumbnail': imageThumbnailLink.attrs['src'],
          'description': article.find('.fc-item__standfirst', first=True).text.strip(),
        }
        qlist.append(item)

    return qlist

  def scrapeSingle(self, tag):
    url = 'https://www.theguardian.com/uk';

    s = HTMLSession()
    r = s.get(url)

    articles = r.html.find('.fc-item__container')

    for article in articles:
      articleLink = article.find('a.js-headline-text', first=True)
      hrefLink = articleLink.xpath('//a', first=True)
      thumbnailLink = article.find('.fc-item__image-container > picture > img', first=True)
      description = article.find('.fc-item__standfirst', first=True)

      fullLinkString = hrefLink.attrs['href']
      if (tag in fullLinkString):
        print(fullLinkString)
        r = s.get(fullLinkString)
        break
    
    sections = r.html.find('.article-body-commercial-selector > p')

    contentSection = [] 

    for content in sections:
      contentSection.append(content.text)

    if (not sections):
      sections = r.html.find('.dcr-1wj398p > li > p')
      for content in sections:
        contentSection.append(content.text)
    
    title = r.html.find('h1.dcr-125vfar', first=True).text.strip()
    subTitle = r.html.find('div.dcr-u4zu7g  > p', first=True).text.strip()
    imageQuote = r.html.find('span.dcr-19x4pdv', first=True).text.strip()
    image = r.html.find('img.dcr-1989ovb', first=True)
    imageLink = image.xpath('//img', first=True)

    article = {
      'title': title,
      'subTitle': subTitle,
      'contentSection': contentSection,
      'imageQuote': imageQuote,
      'img': imageLink.attrs['src'],
    }

    return article