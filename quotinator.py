import click, json, subprocess, os
from dailyquote import quoteNext, statCheck, validate_json_format, mod_corrector, quoteStop


PWD = os.path.dirname(__file__) + "\\"

@click.group()
def quotinator():
    pass


@click.command(help="Used to set up the initial configuration before the quotinator is scheduled.")
@click.option('-fp', '--filepath', type=click.Path(exists=True), default="settings.json",
              prompt="Enter the quote json file to be imported",
              help="Enter the quote json file to be imported")
@click.option('-mo', '--modifier', default=30,
              prompt="Enter multiples of 5 as minutes of interval",
              help="Takes input as multiples of 5 minutes for interval between the notifications")
@click.option("-s/-ns", "--status/--nostatus", type=click.BOOL, default=False,
              help="Displays the current configuration setup")
def setup(filepath, modifier, status):
    with open("settings.json", "r") as f:
        data = json.load(f)
    data["filepath"] = filepath
    data["modifier"] = mod_corrector(modifier)
    with open('settings.json', 'w') as f:
        json.dump(data, f, indent=3)

    if status:
        statCheck()
    
 
@click.command(help="Used to configure the settings with specificity. Also displays the current configuration.")
@click.option('-fp', '--filepath', type=click.Path(exists=True),
              help="Enter the quote json file to be imported")
@click.option('-mo', '--modifier',
              help="Takes input as multiples of 5 minutes for interval between the notifications")
@click.option("-s/-ns", "--status/--nostatus", type=click.BOOL, default=False,
              help="Displays the current configuration setup")
def set(status, filepath = "settings.json", modifier = None):

    with open("settings.json", "r") as f:
        data = json.load(f)

    if filepath is not None:
        data["filepath"] = filepath
    if modifier is not None:
        data["modifier"] = mod_corrector(int(modifier))
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
    with open("settings.json", "w") as f:
        json.dump(data, f, indent=3)
    statCheck()

@click.command(help = "Schedules the task created")
def start():
    with open("settings.json", "r") as f:
        data = json.load(f)
    if data["filepath"] != "settings.json":
        if not os.path.exists(data["filepath"]):
            click.echo("The given filepath does not exist, please rectify and try again.")
            return False
        with open(data["filepath"], "r") as f:
            content = json.load(f)
        
        result = validate_json_format(content)
        if result != True:
            click.echo(result)
            click.echo("ERROR: Please rectify and try again")
            return False
    
    task = f"py {PWD}dailyquote.py"

    process = subprocess.run(task, shell=True, text=True, capture_output=True)
    click.echo(f"{process.stdout}\n{process.stderr}")
    click.echo(quoteNext())


@click.command(help="Stop the running Quotinator")
def stop():
    if click.confirm("Are you sure about stopping the Quotinator?"):
        click.echo(quoteStop())
    else:
        click.echo("Command aborted!")

@click.command(help="shows the current parameters for the app")
def status():
    statCheck()

quotinator.add_command(setup)
quotinator.add_command(set)
quotinator.add_command(reset)
quotinator.add_command(start)
quotinator.add_command(stop)
quotinator.add_command(status)

if __name__ == "__main__":
    quotinator()
    

