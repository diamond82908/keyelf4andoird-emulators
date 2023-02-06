"""
     This file is part of Keyelf4android-emulators.

    Keyelf4android-emulators is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    Keyelf4android-emulators is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Keyelf4android-emulators. If not, see <https://www.gnu.org/licenses/>. 
"""
import io

ADB_TAP_COMMAND_FORMAT = "input tap {x} {y}\n"
ADB_SWIPE_COMMAND_FORMAT = "input swipe {x1} {y1} {x2} {y2} {duration}\n"

class InputMessageSender:
    """
    Send Message to adb shell in order to simulate input.
    NOTICE: This sender cannot tell if the arguments are valid and whether the action is executed or not.
    """
    def __init__(self) -> None:
        self.reset()

    def _check_bound(self) ->None:
        if not self._is_bound:
            raise Exception("Sender has not been bound yet")

    def bind(self, adb_stdin: io.TextIOWrapper) -> None:
        """
        Bind this instance to the stdin of a adb process.
        adb_stdin: the stdin of the adb shell process
        """
        
        if not "wb" in adb_stdin.mode:
            raise ValueError(f'The argument {adb_stdin} is not standard input of any process.')
        self._adb_stdin = adb_stdin
        self._is_bound = True

    def reset(self) -> None:
        """
        Reset all the fields of the instace. The instance will no longer be bound the adb shell process.
        """
        self._adb_stdin = None
        self._is_bound = False

    def send_tap_message(self, x: int, y: int) -> None:
        """send a message to tap the position (x, y) of the screen"""
        self._check_bound()
        self._adb_stdin.write(ADB_TAP_COMMAND_FORMAT.format(x=x, y=y).encode(encoding="ASCII", errors="strict"))
        self._adb_stdin.flush()

    
    def send_swipe_message(self, x1: int, y1:int, x2: int, y2: int, time_in_millisecond: int) -> None:
        """send a message to swipe the screen from (x1, y1) to (x2, y2) within time_in_millisecond"""
        self._check_bound()
        self._adb_stdin.write(ADB_SWIPE_COMMAND_FORMAT.format(x1=x1, y1=y1, x2=x2, y2=y2, duration=time_in_millisecond).encode(encoding="ASCII", errors="strict"))
        self._adb_stdin.flush()