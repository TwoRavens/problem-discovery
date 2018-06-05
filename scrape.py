import requests
import bs4
import json

years = range(2014, 2019)
storage_path = './articles.json'

wiley_url = "https://onlinelibrary.wiley.com"
proxy_url = "https://onlinelibrary-wiley-com.libproxy.utdallas.edu"


def process_issue(extension, issue):
    links = {}
    issue_html = bs4.BeautifulSoup(requests.get(wiley_url + extension).content, "lxml")
    for article in issue_html.findAll("div", {"class": "issue-item"}):

        if not article.find("a", {"title": "Full text"}):
            continue

        authors = []
        for auth_div in article.find("ul", {"class": "loa-authors-trunc"}).children:
            if type(auth_div) == bs4.element.NavigableString:
                continue

            authors.append({
                "name": auth_div.find("a")['title'],
                "url": wiley_url + auth_div.find("a")['href']
            })

        links[article.find("a", {"class": "issue-item__title"})['href']] = {
            "attributes": {
                "issue": issue,
                "title": article.find("a", {"class": "issue-item__title"}).find("h2").text,
                "authors": authors,
                "publish_date": list(article.find("li", {"class": "ePubDate"}).children)[1].text,
                "full_text": proxy_url + article.find("a", {"title": "Full text"})['href']
            },
            "data": []
        }

    return links


def process_year(year):
    links = []
    year_html = bs4.BeautifulSoup(requests.get(wiley_url + "/loi/15405907/year/" + str(year)).content, "lxml")
    for issue in year_html.find("ul", {"class": "rlist loi__issues"}).children:
        links.append(issue.find("a", {"title": "go to "})['href'])

    return links


if __name__ == '__main__':
    records = {}
    for year in years:
        records[year] = {}
        for issue in process_year(year):
            records[year] = {**records[year], **process_issue(issue, issue)}

    with open(storage_path, 'w') as file:
        json.dump(records, file)
