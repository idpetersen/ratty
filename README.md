# Ratty [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description

A remote admistration tool written in python with a malware wrapper that spreads and infects other machines on a local network. 

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contributing](#contributing)
- [Developers](#developers)
- [Questions](#questions)

## Installation

- Clone [this repo](https://github.com/idpetersen/ratty) from my Github to the users computer by running the command in the terminal.

`git clone <repo>`

- The user will need to have some flavor of linux that supports Python 3.10.5

- The other machines on the network will need to also be some flavor of linux, mint is preffered

- The victim machines will need to have [pyautogui](https://pyautogui.readthedocs.io/en/latest/install.html#linux) installed.

## Usage

- To use this RAT the victim machine will need to have the `malware.py` installed on their computer and it needs to be executed.

- The user computer will need to have a python webserver hosted on it, to do so, the command is `python3 -m http.server`

- The `rat_client.py` file needs to have the host IP as it's connection IP. The user can change it at the bottom of the file.

- Then the user computer needs to execute the `rat_server.py`.

- To execute, move file to victim machine and in a terminal the following commands are needed. `chmod +x malware.py` proceeded with `./malware.py`


## License

<p>
MIT License

Copyright &copy; Isaac Petersen 2022

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

  </p>

## Contributing

To contribute, please contact me via [Github](https://www.github.com/idpetersen) or [email](mailto:isaac.petersen5@gmail.com)

## Developers

This project was created by [me](https://github.com/idpetersen) and [mike](https://github.com/MikeBeckemeyer)

## Questions

Contact me via [Github](https://www.github.com/idpetersen) or [email](mailto:isaac.petersen5@gmail.com)
