import json, subprocess, os, click


PWD = os.path.dirname(__file__) + "\\"

def quoteNext():
    process = subprocess.run("schtasks /QUERY /TN quotinator", shell=True, text=True, capture_output=True)
    return process.stdout

def statCheck():
    with open("settings.json", "r") as f:
        data = json.load(f)
        click.echo("-------------------------------")
        click.echo("Status")
        click.echo("-------------------------------")
        click.echo(f"Filepath: \t{data['filepath']}")
        click.echo(f"Modifier: \t{data['modifier']}")
        click.echo("-------------------------------")
        click.echo(quoteNext())

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
                return "Character length limit exceeded for one of the quote titles"
        # If all checks pass, the JSON is in the expected format
        return True

    except json.JSONDecodeError:
        return "Couldn't parse the JSON file"


def quoteDaily():
    with open("settings.json", "r") as f:
        data = json.load(f)

    min = data['modifier']

    filepath = PWD + data["filepath"]

    task_today = f"schtasks /CREATE /TN quotinator /TR \"py {PWD}quotation.py {filepath}\" /SC MINUTE /MO {min} /ET 23:59 /F"

    
    process = subprocess.run(task_today, shell=True, text=True, capture_output=True)
    print(process.stdout)


if __name__ == "__main__":
    quoteDaily()


