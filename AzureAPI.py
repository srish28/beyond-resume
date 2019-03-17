import requests
import docx2txt
import json

# resume = open('C:\\Users\\srish\\Desktop\\Job Related\\Resumes\\SrishtiResume.docx', 'rb')


def getKeywords(resume):
    # coverletter = open('C:\\Users\\srish\\Desktop\\Job Related\\Cover Letters\\Coverletter.docx', 'rb')
    # cov = docx2txt.process(coverletter)
    res = docx2txt.process(resume)
    text = res

    url = "https://eastus.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases"

    data = {
    "documents": [
    {
    "language": "en",
    "id": "1",
    "text": text
    }
    ]
    }

    headers = {
    "Ocp-Apim-Subscription-Key": "c23eff5cda374f68b12e5156b28dd382",
    "Content-Type": "application/json",
    "Accept": "application/json"
    }
    data = requests.post(url, data=json.dumps(data), headers=headers)

    data_read = json.loads(data.text)
    keyPhrases = [i['keyPhrases'] for i in data_read['documents']][0]
    return keyPhrases