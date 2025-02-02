from bs4 import BeautifulSoup
import requests
# A class to represent a Webpage
# If you're not familiar with Classes, check out the "Intermediate Python" notebook

# Some websites need you to use proper headers when fetching them:
headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:

    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

url = "https://edwarddonner.com"
url = "http://quotes.toscrape.com"
url = "https://www.makemytrip.com"

ed = Website(url)

print(ed.title)
print(ed.text)

system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt

print(user_prompt_for(ed))


messages = [
    {"role": "system", "content": "You are a snarky assistant"},
    {"role": "user", "content": "What is 2 + 2?"}
]
response = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.2",
    "prompt": "What is 2 + 2?",
    "system": "You are a rude assistant",
    "stream": False
})

print(response.json()["response"])


def messages_for(website):
    system_prompt = "You are a helpful assistant."  # Adjust as needed
    user_prompt = user_prompt_for(website)  # Assuming this function generates a prompt

    return {
        "model": "llama3.2",  # Change this to match your installed Ollama model
        "system": system_prompt,
        "prompt": user_prompt,
        "stream": False
    }

print(messages_for(ed))

ollama_payload = messages_for(ed)

def summarize(url):
    website = Website(url)
    response = requests.post("http://localhost:11434/api/generate", json=ollama_payload
    )
    return response.json()["response"]


print(summarize(url))
