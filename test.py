url = "https://titanic.kub.sspcloud.fr/predict?sex=female&age=29&fare=16.5&embarked=S"
import requests

request = requests.get(url)
print(request.text)
