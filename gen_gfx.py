# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# 04-22-2019    Jeremiah Knol
#
# Generates binary graphics tables input from a file of ASCII-art-style graphics
#
# Feel free to edit and re-distribute this software!
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#
# Example use: python gen_gfx.py gfx_input.txt gfx_output
# Where 'gfx_input.txt' is your graphics table file,
# and 'gfx_output' is the prefix for the output files.
#
# 'gfx_input.txt' should be set up as following:
#
#   There should be no empty lines at the start of the file.
#
#   The first character is used as the 'on bit' for your graphics tables.
#   The next characters(s) is the height for the graphics:
#   $5          --->    'on' char = $        graphics height = 5
#
#   The next line starts the formatting options for the graphics tables that
#   will be outputted. You can add as many as you want, and each format will
#   output its own file.
#
#   Every format is defined by 9 characters. The first 8 determine the layout of
#   the bits in each byte of the table, and the last byte is either a '+' or '-'
#   for standard vs upside-down order of the bytes within the table.
#
#   For the 8-character bit layout, you can either use data from the graphics
#   tables, or use set/clear bits. 's' is used for set, 'c' for clear.
#
#   You can use '7' through '0' for bits D7 through D0 of the graphics:
#   76543210
#
#   You can also invert graphics by using Shift for numbers 7-0:
#   &^%$#@!)
#
#   As an example, for 3-bit-wide playfield graphics for the Atari 2600,
#   you may want something like this:
#   210c210c-   --->    outputs 2 copies of the same graphics
#   c021c021-   --->    same as above, but mirrored for reversed playfield
#   (Note the '-' for upside-down graphics tables)
#
#   After the list of output formats, leave an empty line.
#
#   Lastly, list the graphics table, with each sprite the correct height,
#   and seperated by blank lines:
#
#   $$$
#   $_$
#   $_$
#   $_$
#   $$$
#
#   $$_
#   _$_
#   _$_
#   _$_
#   $$$
#
#   $$$
#   __$
#   $$$
#   $__
#   $$$
#
#   etc.
#
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>



import sys

class Format:
    """Graphics table format options"""

    def setLayout(self, layout):
        self.layout = layout

    def setDirection(self, direction):
        self.direction = direction



if len(sys.argv) < 3:
    print('ERROR: You must provide an input file and output filename prefix\n')
    print('    Example: python gen_gfx.py input.txt output')
    print("    This would output files named 'output0.bin', \
'output1.bin', 'output2.bin' etc.\n")
    raise

try:
    file = open(sys.argv[1], 'r')
except:
    raise

set_symbol = file.read(1)
char_height = int(file.readline()[:-1])

formats = []
line = file.readline()
while line != '\n':
    new_format = Format()
    new_format.setLayout(line[:-2])
    new_format.setDirection(line[8])
    formats.append(new_format)

    line = file.readline()

chars = []
line = file.readline()[:-1]
while line != '':
    char_gfx = []
    for i in range(char_height):

        char_val = 0
        for j in range (len(line)):
            if line[j] == set_symbol:
                char_val += 2**((len(line)-1)-j)

        char_gfx.append(char_val)
        line = file.readline()[:-1]

    chars.append(char_gfx)
    line = file.readline()[:-1]

file.close()

for f in range(len(formats)):

    try:
        file = open(sys.argv[2] + str(f) + '.bin', 'wb')
    except:
        raise

    for char in chars:

        if formats[f].direction == '-':
            x = -1
        else:
            x = 1
        for gfx in char[::x]:

            new_byte = 0
            for j in range(8):
                b = formats[f].layout[7-j]
                
                if b == 's':
                    new_byte += 2**j
                elif b >= '0' and b <= '7':
                    if gfx & (2**int(b)):
                        new_byte += 2**j
                else:
                    i = ')!@#$%^&'.find(b)
                    if i >= 0 and (gfx & (2**i)) == False:
                        new_byte += 2**j

            file.write(bytes([new_byte]))

    file.close()

