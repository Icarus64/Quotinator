from plyer import notification
from dailyquote import createIndex
import json, sys, os, pyautogui, requests


pyautogui.hotkey("win", "down")
PWD = os.path.dirname(__file__) + "\\"

def show_notification(title, message, index):
    updateIndex(index)
    notification.notify(
        title=title, message=message, app_name="DoneQuote", timeout=15, ticker="DONE"
    )

    return True

def remoteQuotation():
    url = 'https://zenquotes.io/api/random'
    try:
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            quote = json.loads(response.text)
            notification.notify(
                title = quote[0]["a"], message=quote[0]["q"], app_name="DoneQuote", timeout=15, ticker="DONE"
            )
            return True
        else:
            print("Some error occured, switching to local quote")
            return False
    except Exception as e:
        print(e)
        return False


def quotation(payload, remote):
    index = getIndex()
    if remote:
        result = remoteQuotation()
        if result:
            return result
    
    if index >= len(payload):
       update = 0
    else:
       update = index + 1
    
    try:
        payload[index]
    except:
        index = 0
        update = index + 1

    return show_notification(
        title=payload[index]["title"], message=payload[index]["message"], index=update
    )

def getIndex():
    if os.path.exists(PWD +'index.json'):
        with open(PWD + "index.json", "r") as file:
          return json.load(file)['index']
    else:
        with open(PWD + "index.json", "w") as file:
          json.dump({"index": 0}, file)
          return 0
          
def updateIndex(index):
    if os.path.exists(PWD + 'index.json'):
        with open(PWD + "index.json", "w") as file:
          json.dump({"index": index}, file)

if __name__ == "__main__":
    with open(PWD + "settings.json", 'r') as f:
        content = json.load(f)
    remote = content["remote"]
    if 'settings.json' in sys.argv[1]:
        data=content['done_manifesto']
    else:
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
    quotation(data, remote)
    