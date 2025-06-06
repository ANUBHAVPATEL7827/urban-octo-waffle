import requests
from bs4 import BeautifulSoup

def scrape_jobs():
    # Example: SarkariResult (Govt jobs)
    url = "https://www.sarkariresult.com/latestjob.php"
    jobs = []

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.select(".post a")

        for link in links[:10]:  # Limit to top 10 for testing
            title = link.text.strip()
            job_url = link['href']
            jobs.append((title, job_url))
    except Exception as e:
        print(f"[Scraper Error] {e}")

    return jobs
