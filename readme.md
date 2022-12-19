# What is it
This project helps you convert chisel3 code to btor2 code.

# Dependencies
- jdk 17
- sbt 1.4.9
- python3

# How to use
1. Clone this project
2. Copy your chisel3 code to the project
3. Change the `chisel_file` in chisel2btor.py code
4. Run `python3 chisel2btor.py`

or you can change the line 55 in chisel2btor.py to `converter = Converter(chiselfv_dir)`, which makes you can pass parameters by console.
