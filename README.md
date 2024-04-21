# Twitch Game Control Bot

This project allows Twitch viewers to control a game via chat commands using a virtual Xbox 360 controller. The bot handles Twitch chat commands, simulates button presses and joystick movements, and updates an OBS stream with the current command queue.

## Features

- Twitch chat integration for game control commands.
- Virtual gamepad simulation with configurable button mapping.
- Real-time OBS update of command queue.

## Requirements

- Python 3.6+
- twitchio
- dotenv
- vgamepad
- obswebsocket
- asyncio

## Installation

1. **Clone the repository**

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

## Setup

### Environment Variables

Create a .env file in the project directory and add the following keys:

```makefile
ACCESS_TOKEN=<your-twitch-access-token>
CHANNEL=<your-twitch-channel>
OBS_WS_HOST=localhost
OBS_WS_PORT=4455
OBS_WS_PW=salasana
```

## Configure OBS

Ensure OBS is configured to accept WebSocket connections.
Create a text source named CommandText in your OBS scene.

## Usage

Run the bot with the following command:

```bash
python -m twitch_game_control_bot
```

## Commands

Commands
Gamepad Commands
?a: Simulate pressing the "A" button
?b: Simulate pressing the "B" button
?l: Simulate pressing the "L" button
?r: Simulate pressing the "R" button
?select: Simulate pressing the "Select" button
?start: Simulate pressing the "Start" button
Movement Commands
?move up [tiles]: Simulate moving up [tiles] times
?move down [tiles]: Simulate moving down [tiles] times
?move left [tiles]: Simulate moving left [tiles] times
?move right [tiles]: Simulate moving right [tiles] times

## Contributing

Contributions are welcome! Feel free to open a pull request with your proposed changes.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
