# DBMS Concurrency Control and Recovery Implementation

Proof of concept for implementing concurrency control and recovery mechanisms in a Database Management System (DBMS). This project aims to demonstrate how these critical features can be effectively integrated to ensure data integrity and consistency during simultaneous transactions and system failures. This project is written in Python, and simulates the algorithms implemented in Database Management Systems, such as Two Phase Locking Protocol, MV Timestamp Procol, and Validation Protocol.

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
