# Mouse-Board v3 by Faralaks
Write/Run step-by-step mouse and keyboard emulation macros!

A strange but native dark GUI. This project is mainly based on tkinter and PyAutoGUI

It was created especially for Windows but other platforms are potentially supported.

# Program features
- Writing macros to emulate mouse clicks and keyboard.
- Waiting for image on screen.
- Clicking on images on screen.
- Taking a screenshot and recording clicks on it or finding images.
- Cut out part of the screenshot and save it as image for later usage.
- Adding an interval between commands.
- Paste text from file.
- Find file on computer.
- Saving macros to files.
- Logging to a text file.


# Usage (Windows)
1. Download last realise binary from [Releases page](https://github.com/Faralaks/mouse-board/releases).
2. Execute it:) You may need to give permission to launch it.
3. Write macros in main text field (See [Language](#Language)).
4. Press RUN Macros button.
5. Enjoy!

# Language
- There are many commands available for you now.
- Each command begins with new line. It means that all commands are divided by newline symbol `\n`.
- By default, parameters are divided by `+` symbol, but you can change it in top menu.
- First word in line always command word then parameters.
- Last parameter may be Delay before next command.
- Below you can see list of commands and their syntax.

# Commands and their Syntax
- click - Click on screen

`click+x+y+btn`

**Parameters:** x, y - coordinates. btn - `left` or `right` means mouse button.

- dclick - Double left mouse button click on screen

`dclick+x+y`

**Parameters:** x, y - coordinates.



- write - Paste text

`write+text`

**Parameters:** text - Some text.

- file - Paste text from text file

`file+path`

**Parameters:** path - file path. Use `.` to specify relative path.

- wait - Wait some seconds

`wait+delay`

**Parameters:** delay - seconds to wait.

- Move - Move cursor by relative coordinates

`move+relative_x+relative_y+time`

**Parameters:** relative_x and relative_y relative coordinates. time - cursor movement time.

- Moveto - Move cursor to coordinates

`moveto+x+y+time`

**Parameters:** x and y coordinates. time - cursor movement time.

- Press - Press keyboard buttons

`press+keys`

**Parameters:** keys - list of keyboard buttons divided by space symbol.

- Cimage - click in the middle of image on screen

`cimage+file_path+confidence+btn+clicks_count+clicks_interval`

**Parameters:** file_path - path to the image file. confidence - accuracy of the search (can be between 0 and 1). 
btn - `left` or `right` means mouse button. clicks_count - how many times do It has to click.
clicks_interval - interval in seconds between clicks.

- Dimage - double left mouse click in the middle of image on screen

`dimage+file_path+confidence`

**Parameters:** file_path - path to the image file. confidence - accuracy of the search (can be between 0 and 1). 


- Wimage - wait until the image appears on the screen

`wimage+file_path+confidence+find_interval+time_limit`

**Parameters:** file_path - path to the image file. confidence - accuracy of the search (can be between 0 and 1). 
find_interval - interval in seconds between searches.
time_limit - maximum seconds to wait for image.

- Aimage - click in the center of each found image on screen

`aimage+file_path+confidence+btn+clicks_count+clicks_interval+find_interval`

**Parameters:** file_path - path to the image file.
confidence - accuracy of the search (can be between 0 and 1). 
btn - `left` or `right` means mouse button.
clicks_count - how many times do It has to click.
clicks_interval - interval in seconds between clicks.
find_interval - interval in seconds between searches.


# Make now
- Program output redirects to log.txt which is created next to the executable file.
- Empty line equal `wait+0`
- If the program cannot bring the last parameter to float or the number of parameters is equal to the number of parameters of command without wait parameter, it sets the Default Delay.
- Default Delay by default:) equal 0.1 sec, but you can change it in top menu.
- After each command the program goes to sleep (time.sleep function) for the specified or default delay.
- You can use Find File button to automatically pate file path.
- You can use ScreenShot button to record clicks, test image finding or cut out part of screenshot.
- Before start macros program checks it.
- It checks the correctness of the commands and parameters and the existence of the specified files.
- If errors occur, the corresponding messages are displayed.
- Text pasts by `ctrl+v` or `commnd+v`. It means that text pasts from clipboard. If you had something in the clipboard, it will remain there.

# Examples
- `wait+4` - Just waits 2 seconds.
- `click+1000+500+left+0.1` - Clicks left mouse button on point (1000, 500) with delay 0.1 sec before next command.
- `click+800+900+right+0` - Clicks right mouse button on point (800, 900) with delay 0 sec before next command.
- `write+This is the best project in the whole world!` - pats this text with default delay before next command.
- `write+Is it the best project in the whole world?+1` - pats this text with 1 sec delay before next command.
- `file+C:\data\file.txt` - pasts text content from file (absolute path) with default delay before next command.
- `file+.\file.txt+22` - pasts text content from file (relative path) with 22 sec delay before next command.