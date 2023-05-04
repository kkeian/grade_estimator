# Grade Estimator

Stupid little CLI program that simulates passing score combos for weighted grade categories.  
Originally intended for simulating exam score combos. Works OK for # categories <= 2.  
**Always enter the tool's score combos into actual grade webpage to check they are valid combos.**

## Setup on your computer
1. Create "classes/" directory inside the repo and fill it with .json files for your current semester.
> JSON file layout needs to be exactly like example_class.json
2. Ensure PASSING_PERCENT value is adjusted to match the passing percentage (C- lowest %) for the class you're going to simulate.
3. Make main.py executable on your machine (e.g. `chmod +x main.py` for Mac and Linux).
4. Run main.py (e.g. `./main.py` on Mac and Linux).
5. Follow prompts.
6. Check that output score combos actually result in passing % by entering the score combo of interest on your class's Grades webpage.

## Contributing
Contributions and improvements are welcome.

If you found this tool useful and have a way to improve it, please fork the repo and submit a PR.
<br>
I'm the only one managing this repo and am a full-time student, but this project is particularly useful to me so I will respond to PR's within a day or two at most.

## License
[GPLv2](LICENSE)