from plyer import notification
import json, sys, os, pyautogui


pyautogui.hotkey("win", "down")
PWD = os.path.dirname(__file__) + "\\"

def show_notification(title, message, index):
    updateIndex(index)
    return notification.notify(
        title=title, message=message, app_name="DoneQuote", timeout=15, ticker="DONE"
    )


def quotation(payload):
    index = getIndex()
    if index+1 >= len(payload):
       update = 0
    else:
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
    try:
        if 'settings.json' in sys.argv[1]:
            with open(sys.argv[1], 'r') as f:
                data=json.load(f)['done_manifesto']
        else:
            with open(sys.argv[1], 'r') as f:
                data = json.load(f)
        quotation(data)
    except Exception as e:
        print(e)