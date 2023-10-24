# Quotinator - Daily Quote Notifier

Quotinator is a simple Python application for daily quote notifications. It allows you to configure a JSON file with a list of quotes, and it will display a new quote notification at regular intervals throughout the day. Comes with a set of principles from the Done Manifesto as default.

## Features

- Set up the initial configuration for your quote notifications.
- Configure notification intervals (in multiples of 5 minutes).
- Easily view and update your current configuration.
- Reset all parameters to default values.
- Start the daily quote notification task.
- Check the current status and parameters of the app.

## Getting Started

1. Clone this repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Run the main program by executing `quotinator.py` using Python.

## Usage

### Initial Configuration

Before you start receiving daily quotes, you need to set up the initial configuration:

```
python quotinator.py setup
```

You'll be prompted to enter the path to your JSON file containing quotes and the interval for notifications (in multiples of 5 minutes).

### Configuration Settings

To configure or update your settings, use the following command:

```
python quotinator.py set
```

You can choose to update the JSON file path or the notification interval.

### Start Daily Quote Notifications

To start receiving daily quote notifications, use:

```
python quotinator.py start
```

This command will schedule the task to display quotes throughout the day.

### View Current Status

To check the current status and parameters of the app, use:

```
python quotinator.py status
```

## Reset to Default

If you want to reset all parameters to their default values, run:

```
python quotinator.py reset
```

## Stop the scheduled task

if you want to stop the scheduled task, run:

```
python quotinator.py stop
```

## JSON File Format

The JSON file containing your quotes should have the following format:

```json
[
    {
        "title": "Quote Title 1",
        "message": "Quote Message 1"
    },
    {
        "title": "Quote Title 2",
        "message": "Quote Message 2"
    },
    ...
]
```

## Example JSON

```json
[
    {
        "title": "Inspirational Quote",
        "message": "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle."
    },
    {
        "title": "Motivational Quote",
        "message": "Don't watch the clock; do what it does. Keep going."
    }
]
```

## Important Note

Make sure your JSON file follows the specified format, and the path to the JSON file is correctly configured in the settings.
quotinatorV2 is a different take on the Quotinator project that's on hold for now, please go through it and tinker around if you would like to.

## Authors

- Saianand

Feel free to contribute or suggest improvements to this project. Enjoy your daily dose of inspiration and motivation with Quotinator!