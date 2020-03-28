from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

class Tokenizer:
    def __init__(self):
        self.title = []
        self.strong = []
        self.headers = []

    def tokenize(self, file):
        soup = BeautifulSoup(file, 'lxml')

        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text("|", strip=True)

        if soup.find('meta', attrs={'name': 'description'}) != None:
            description = soup.find('meta', attrs={'name': 'description'}).get("content")
        else:
            description = ""

        if soup.find('meta', attrs={'name': 'date'}) != None:
            date = soup.find('meta', attrs={'name': 'date'}).get("content")[5:17].replace(" ", "") + " "
        else:
            date = ""

        if soup.find('title') != None:
            title = soup.find('title')
            self.title = self._lemmatize(str(title.string))

        if soup.find("strong") != None:
            strong = soup.find('strong')
            self.strong = self._lemmatize(str(strong.string))

        headers = ""
        for tags in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
            headers += tags.text

        self.headers = self._lemmatize(headers)

        text = date + description + text

        return self._lemmatize(text)

    def _lemmatize(self, text):
        stopWords = set(stopwords.words('english'))
        tokens = []

        for token in word_tokenize(text):
            token = token.lower()
            if token not in stopWords and token.isalnum() and not token.isnumeric() and len(token) > 1:
                tokens.append(WordNetLemmatizer().lemmatize(token))
        return tokens
















