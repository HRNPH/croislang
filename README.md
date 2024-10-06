# Croisslang
Croisslang is a stupid programming language inspired by croissants. It allows you to create, manipulate, and combine "croissants" (binary data) and "bake" them through various operations.

## Features
- Define memory size using an "Oven."
- Create croissants (binary data) and store them in trays.
- Flip, combine, and manipulate trays of croissants.
- Serve trays of croissants after performing operations.

### Syntax Overview

#### Memory Definition
Before you begin, you must specify the memory size for your operations using the `Oven` syntax:
```
Oven<8>
```
This defines that the memory size is 8 bits.

#### Prepare Croissant
To create a croissant (a set of binary data), use the `Prepare` keyword:
```
Prepare <1,0,1,1> into TrayA
```
This creates a binary croissant `[1, 0, 1, 1]` and stores it in `TrayA`.

#### Combine Trays
You can combine two trays of croissants into a new tray:
```
Combine TrayA with TrayB into TrayC
```
This combines `TrayA` and `TrayB` and stores the result in `TrayC`.

#### Flip Croissant
You can flip a croissant at a specific position using the `Flip` keyword:
```
Flip TrayC at 2
```
This flips the bit at position `2` in `TrayC`.

#### Serve a Tray
After performing operations, you can serve the final tray:
```
Serve TrayC
```

### Example Code
Here's an example `.crois` file demonstrating the features:

```croisscript
Oven<8>
Prepare <1,0,1,1> into TrayA
Prepare <0,1,1,0> into TrayB
Combine TrayA with TrayB into TrayC
Flip TrayC at 2
Serve TrayC
```

### Installation and Setup
To get started with Croisslang, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/croisslang.git
   cd croisslang
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Croisslang script:
   ```bash
   python croisslang.py ./examples/binary_add.crois
   ```

### Running Croisslang
To run a `.crois` file, use the CLI tool. Here is an example:

```bash
python croisslang.py ./examples/binary_add.crois
```

The script will parse and execute the Croisslang code, producing the desired operations on croissants and trays.

### Examples

#### Example 1: Simple Addition Simulation
This example simulates adding two 4-bit binary numbers:
```croisscript
Oven<4>
Prepare <1,1,0,1> into TrayA  # 13 in binary
Prepare <0,0,1,1> into TrayB  # 3 in binary
Combine TrayA with TrayB into TrayC
Flip TrayC at 1
Serve TrayC
```

#### Example 2: Bitwise Manipulation
This example flips and combines multiple trays:
```croisscript
Oven<4>
Prepare <1,0,0,1> into TrayA
Prepare <1,1,0,0> into TrayB
Flip TrayA at 2
Combine TrayA with TrayB into TrayC
Serve TrayC
```

---