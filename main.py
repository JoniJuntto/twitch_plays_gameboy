import os
from twitchio.ext import commands
from dotenv import load_dotenv
import vgamepad as vg
import time
from obswebsocket import obsws, requests
from collections import deque
import threading
import asyncio

gamepad = vg.VX360Gamepad()
load_dotenv()


last_command_time = {}
input_buffer = deque()

button_mapping = {
    "a": vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
    "b": vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
    "l": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    "r": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
    "start": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
    "select": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
}

action_buttons = ["a", "b", "l", "r", "start", "select"]
move_buttons = ["up", "down", "left", "right"]

host = os.getenv("OBS_WS_HOST")
port = os.getenv("OBS_WS_PORT")
password = os.getenv("OBS_WS_PW")
source_name = "CommandText"
new_text = "Hello, World!"


def update_obs_command_queue():
    commands_list = "\n".join([desc for desc, _ in list(input_buffer)])
    send_obs_command(commands_list if commands_list else "No commands in queue")


async def handle_commands():
    while True:
        if input_buffer:
            _, command = input_buffer.popleft()
            await command()
            update_obs_command_queue()
        time.sleep(0.1)


def move_to_direction(direction: str, tiles: int = 1):
    if direction == "up":
        x = 0.0
        y = 1.0
    elif direction == "down":
        x = 0.0
        y = -1.0
    elif direction == "left":
        x = -1.0
        y = 0.0
    elif direction == "right":
        x = 1.0
        y = 0.0

    for _ in range(tiles):
        gamepad.left_joystick_float(x_value_float=x, y_value_float=y)
        gamepad.update()
        time.sleep(0.1)
        gamepad.reset()
        gamepad.update()
        time.sleep(0.3)


def send_obs_command(message: str):
    host = "localhost"
    port = 4455
    password = "salasana"

    ws = obsws(host, port, password)
    ws.connect()

    try:
        ws.call(
            requests.SetInputSettings(
                inputName="CommandText", inputSettings={"text": message}
            )
        )
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ws.disconnect()


async def press_action_button(self, button: str, author: str):
    send_obs_command(f"{author} pressed {button}")
    gamepad.press_button(button=button_mapping[button])
    gamepad.update()
    time.sleep(self.delay)
    gamepad.release_button(button=button_mapping[button])
    gamepad.update()


async def press_move_button(self, author: str, direction: str, tiles: int = 1):
    current_time = time.time()
    if (
        author not in last_command_time
        or (current_time - last_command_time[author]) > self.command_cooldown
    ):
        if direction in ["up", "down", "left", "right"]:
            if tiles > 10:
                tiles = 10
            if tiles < 1:
                tiles = 1
            move_to_direction(direction, tiles)
            last_command_time[author] = current_time
            print(f"{author}: {direction} {tiles}")
            send_obs_command(f"{author}: {direction} {tiles}")
        else:
            print("Invalid direction!")
    else:
        print("lol")


async def press_button(self, author: str, button: str = "", tiles: int = 1):
    if button in action_buttons:
        input_buffer.append(
            (
                f"{author} press {button}",
                lambda: press_action_button(self, button, author),
            )
        )
    elif button in move_buttons:
        input_buffer.append(
            (
                f"{author} move {button} {tiles}",
                lambda: press_move_button(self, author, button, tiles),
            )
        )
    update_obs_command_queue()


class Bot(commands.Bot):
    delay = 0.1
    command_cooldown = 3

    def __init__(self):
        super().__init__(
            token=os.getenv("ACCESS_TOKEN"),
            prefix="?",
            initial_channels=[os.getenv("CHANNEL")],
        )

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

    @commands.command()
    async def a(self, ctx: commands.Context):
        await press_button(self, ctx.author.name, "a")

    @commands.command()
    async def b(self, ctx: commands.Context):
        await press_button(self, ctx.author.name, "b")

    @commands.command()
    async def l(self, ctx: commands.Context):
        await press_button(self, ctx.author.name, "l")

    @commands.command()
    async def r(self, ctx: commands.Context):
        await press_button(self, ctx.author.name, "r")

    @commands.command()
    async def select(self, ctx: commands.Context):
        await press_button(self, ctx.author.name, "select")

    @commands.command()
    async def start(self, ctx: commands.Context):
        await press_button(self, ctx.author.name, "start")

    @commands.command()
    async def move(self, ctx: commands.Context, direction: str, tiles: int = 1):
        await press_button(self, ctx.author.name, direction, tiles)


bot = Bot()
threading.Thread(target=lambda: asyncio.run(handle_commands()), daemon=True).start()
bot.run()
