from requests_html import HTMLSession
from fastapi import HTTPException

class Scraper():
  def scrapeMultiple(self):
    url = 'https://www.theguardian.com/uk';

    s = HTMLSession()
    r = s.get(url)

    articleList = []
    articles = r.html.find('.fc-item__container')

    for article in articles:
      articleLink = article.find('a.js-headline-text', first=True)
      hrefLink = articleLink.xpath('//a', first=True)
      thumbnailLink = article.find('.fc-item__image-container > picture > img', first=True)
      description = article.find('.fc-item__standfirst', first=True)
      
      title = article.find('.fc-item__title', first=True).text.strip()
      if (thumbnailLink and description and ('Live' not in title)):
        imageThumbnailLink = thumbnailLink.xpath('//img', first=True)
        item = {
          'title': title,
          'url': hrefLink.attrs['href'],
          'thumbnail': imageThumbnailLink.attrs['src'],
          'description': article.find('.fc-item__standfirst', first=True).text.strip(),
        }
        articleList.append(item)

    return articleList

  def scrapeSingle(self, tag):
    url = 'https://www.theguardian.com/uk'

    s = HTMLSession()
    r = s.get(url)

    externalLink = ''
    articles = r.html.find('.fc-item__container')

    for article in articles:
      articleLink = article.find('a.js-headline-text', first=True)
      hrefLink = articleLink.xpath('//a', first=True)
      fullLinkString = hrefLink.attrs['href']

      if (tag in fullLinkString):
        r = s.get(fullLinkString)
        externalLink = fullLinkString
        break
    
    sections = r.html.find('.article-body-commercial-selector > p')

    contentSection = [] 

    for content in sections:
      contentSection.append(content.text)

    if (not sections):
      sections = r.html.find('.dcr-1wj398p > li > p')
      for content in sections:
        contentSection.append(content.text)
    
    if (not sections):
      raise HTTPException(status_code=404, detail="Article not found")

    
    # title = r.html.find('h1.dcr-125vfar', first=True)
    title = r.html.find('div[data-gu-name=headline]', first=True).text.strip()
    if (title):
      print(title)

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
      'externalLink': externalLink
    }

    return article