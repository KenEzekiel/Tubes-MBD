# DBMS Concurrency Control and Recovery Implementation

## How to Use
1. Clone or fork this repository
```sh
https://github.com/KenEzekiel/Tubes-MBD
```
2. Use test-case or make your own test case and put it into inputs.txt. 
For the syntax, input: textfile of a schedule, separated by new lines
```sh
Example:
RX(Y)
WX(Y)
XLZ(Y)
SLZ(Y)
UL(Y)
CX
VX
```
3. Run the appropriate algorithm
```shell
python src/<TwoPhaseLockingProtocol, MVTimestampProtocol, or ValidationProtocol>.py
```
4. The CLI program will ask you about the input file and output, enter without .txt extension
```shell
Input file: 2pl
Output file: 2pl_output
```