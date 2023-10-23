import click, json, subprocess, os, datetime


PWD = os.path.dirname(__file__) + "\\"

@click.group()
def quotinator():
    pass

DAYS_OPTIONS = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

def statCheck():
    with open("settings.json", "r") as f:
        data = json.load(f)
        click.echo("-------------------------------")
        click.echo("Status")
        click.echo("-------------------------------")
        click.echo(f"Filepath: \t{data['filepath']}")
        click.echo(f"Modifier: \t{data['modifier']}")
        click.echo(f"Days: \t\t{data['days']}")
        click.echo("-------------------------------")

def mod_corrector(modifier):
    if modifier < 5:
        correction = 5
        click.echo(f"\nDetected invalid input for the modifier option \nmodifier ({modifier}) --> modifier ({correction})")
        return correction
    if modifier % 5 != 0:
        correction = modifier - (modifier % 5)
        click.echo(f"\nDetected invalid input for the modifier option \nmodifier ({modifier}) --> modifier ({correction})")
        return correction
    return modifier

def validate_json_format(data):
    try:
        # Ensure that the parsed JSON is a list
        if not isinstance(data, list):
            return "The given file is not a JSON list"

        # Check each object in the list
        for item in data:
            if not isinstance(item, dict) or "title" not in item or "message" not in item:
                return "Incorrect item format detected in the list, please correct it"
            if len(item["title"]) > 64:
                return "Character length limit exceeded"
        # If all checks pass, the JSON is in the expected format
        return True

    except json.JSONDecodeError:
        return "Couldn't parse the JSON file"

def is_task():
    process = subprocess.run("schtasks /Query /TN quotinator", shell=True, text=True, capture_output=True)
    print(process)
    if 'ERROR' in process.stderr:
        return False
    return True



@click.command(help="Used to set up the initial configuration before the quotinator is scheduled.")
@click.option('-fp', '--filepath', type=click.Path(exists=True), default="settings.json",
              prompt="Enter the quote json file to be imported",
              help="Enter the quote json file to be imported")
@click.option('-mo', '--modifier', default=30,
              prompt="Enter multiples of 5 as minutes of interval",
              help="Takes input as multiples of 5 minutes for interval between the notifications")
@click.option('-d', '--days', type=click.Choice(DAYS_OPTIONS), multiple=True, 
              default=('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'), 
              help="Specifies the days the task should be scheduled on. Default is 7 days of the week")
@click.option("-s/-ns", "--status/--nostatus", type=click.BOOL, default=False,
              help="Displays the current configuration setup")
def setup(filepath, modifier, days, status):
    with open("settings.json", "r") as f:
        data = json.load(f)
        data["filepath"] = filepath
        data["modifier"] = mod_corrector(modifier) 
        data["days"] = days
    with open('settings.json', 'w') as f:
        json.dump(data, f, indent=3)

    if status:
        statCheck()
    
 
@click.command(help="Used to configure the settings with specificity. Also displays the current configuration.")
@click.option('-fp', '--filepath', type=click.Path(exists=True),
              help="Enter the quote json file to be imported")
@click.option('-mo', '--modifier',
              help="Takes input as multiples of 5 minutes for interval between the notifications")
@click.option('-d', '--days', type=click.Choice(DAYS_OPTIONS), multiple=True,  
              help="Specifies the days the task should be scheduled on. Default is 7 days of the week. \nUse the flag multiple times to enter specific days")
@click.option("-s/-ns", "--status/--nostatus", type=click.BOOL, default=False,
              help="Displays the current configuration setup")
def set(status, days, filepath = "settings.json", modifier = None):

    with open("settings.json", "r") as f:
        data = json.load(f)
    
    if filepath is not None:
        data["filepath"] = filepath
    if modifier is not None:
        data["modifier"] = mod_corrector(int(modifier))
    if len(days) > 0:
        data["days"] = days
    with open("settings.json", "w") as f:
        json.dump(data, f, indent=3)
    

    if status:
        statCheck()
        

@click.command(help="Resets all the required parameters to the default values")
def reset():
    with open("settings.json", "r") as f:
        data = json.load(f)
        data["filepath"] = "settings.json"
        data["modifier"] = 30
        data["days"] = DAYS_OPTIONS
    with open("settings.json", "w") as f:
        json.dump(data, f, indent=3)
    statCheck()

@click.command(help = "Schedules the task created")
def start():
    with open("settings.json", "r") as f:
        data = json.load(f)

    today = datetime.date.today().strftime("%a").upper()

    if today in data['days']:
        subprocess.run("py dailyquote.py", shell=True, text=True, capture_output=True)

    task_weekly = f"schtasks /Create /TN quotinator-main /SC WEEKLY /D {',' .join(data['days'])} /ST 00:00 /TR \"py {PWD}dailyquote.py\" /F"
    process = subprocess.run(task_weekly, shell=True, text=True, capture_output=True)
    click.echo(f"{process.stdout}\n{process.stderr}")
    


@click.command(help="shows the current parameters for the app")
def status():
    statCheck()

quotinator.add_command(setup)
quotinator.add_command(set)
quotinator.add_command(reset)
quotinator.add_command(start)
quotinator.add_command(status)

if __name__ == "__main__":
    quotinator()
    

