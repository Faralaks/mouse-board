# Mouse-Board by Faralaks
Write/Run step-by-step mouse and keyboard emulation macros!

A strange but native GUI. This project is mainly based on tkinter and PyAutoGUI

It was created especially for Windows but other platforms are potentially supported.

# Program features
- Writing macros to emulate mouse clicks and keyboadr.
- Taking a screenshot and recording clicks on it.
- Adding an interval between commands.
- Paste text from file.
- Find file on computer.
- Saving macros to files.
- Logging to a text file.


# Usage (Windows)
1. Download last realise binary from [Releases page](https://github.com/Faralaks/mouse-board/releases).
2. Execute it:) You may need to give permission to launch it.
3. Write scripts in main text field (See [Language](#Language)).
4. Press RUN Script button.
5. Enjoy!

# Language
- There are 4 commands available for you now: `click`, `write`, `file` and`wait`. A little later there will be more of them (See [future](#Future))
- Each command begins with new line. It means that all commands are divided by newline symbol `\n`.
- By default, parameters are divided by `@` symbol but u can change it in top menu.
- First word in line as always command word then parameters.
- Last parameter is always Delay before next command.
- Below you can see the syntax of the commands:

# Syntax
- click - Click on screen

`click@x@y@button@delay`

**Parameters:** x, y - coordinates. button - `left` or `right` means mouse button.

- write - Paste text

`write@text@delay`

**Parameters:** text - Some text.

- file - Paste text from text file

`file@path@delay`

**Parameters:** path - file path. Use `.` to specify relative path.

- wait - Wait some seconds

`wait@sec@delay`

**Parameters:** sec - seconds to wait.

# Make now
- Program output redirects to log.txt which is created next to the executable file.
- Empty line equal `wait@0`
- If the program cannot bring the last parameter to float, it sets the Default Delay.
- Default Delay by default:) equal 0.1 sec but u can change it in top menu.
- After each command the program goes to sleep (time.sleep function) for the specified delay.
- You can use Find File button to automatically pate file path.
- You can use ScreenShot button to start clicks recording. It records mouse button and coordinates.
- Before start macros program checks it.
- It checks the correctness of the commands, the presence of points on the screen and the existence of the specified files.
- If errors occur, the corresponding messages are displayed.
- Text pasts by `ctrl+v` or `commnd+v`. It means that text pasts from clipboard. If you had something in the clipboard, it will remain there.

# Examples
- `wait@4` - Just waits 2 seconds.
- `click@1000@500@left@0.1` - Clicks left mouse button on point (1000, 500) with delay 0.1 sec before next command.
- `click@800@900@right@0` - Clicks right mouse button on point (800, 900) with delay 0 sec before next command.
- `write@This is the best project in the whole world!` - pats this text with default delay before next command.
- `write@Is it the best project in the whole world?@1` - pats this text with 1 sec delay before next command.
- `file@C:\data\file.txt` - pasts text content from file (absolute path) with default delay before next command.
- `file@.\file.txt@22` - pasts text content from file (relative path) with 22 sec delay before next command.

# Future
In the future, I want to add some commands:
- move - just moves cursor to point.
- dclick - double click.
- image - click on image on screen.
- wimage - waits before image appears on screen.

Also, I want to add some functionality to ScreenShot button. It should be able to cut out part of the image from the screenshot for the convenience of the image and wimage commands.
