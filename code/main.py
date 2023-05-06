machine_directory = "../machines"
strings_filename = "../strings/strings.txt"
log_filename = "/tm.log"
result_directory = "../results"


def main():
    # Used to read m00 and m01 but can be extended if necessary.
    for i in range(0, 2):
        machine_name = f"m{str(i).zfill(2)}.tm"  # zfill makes it always have at least 2 digits.
        in_directory = machine_directory + "/" + machine_name
        machine = read_machine(in_directory)

        machine_name = machine_name.split('.')[0]  # Prep to change .tm file to .txt file.
        out_directory = result_directory + "/" + machine_name + ".txt"
        log_directory = result_directory + "/" + log_filename
        run_machine(machine, out_directory, log_directory, machine_name)


def run_machine(machine, machine_output_directory, log_directory, machine_name):
    """
    Read all strings from a file into our machine.
    :param machine:
    :param machine_output_directory:
    :param log_directory:
    :param machine_name:
    """
    accept_count = 0
    with open(strings_filename, 'r') as infile, open(machine_output_directory, 'w') as outfile:
        # Each line is a string.
        for string in infile.readlines():
            if '\n' in string:
                string = string[:-1]

            tape = list(string)  # Put each symbol of the string onto the single-tape.
            tape.append('@0')    # Append the blank symbol to the end of tape.
            tape_head = 0        # Refers to the tape pointer, starting at index 0.

            fail_count = 10000   # Failsafe for how many symbols can be read before quitting this string.

            # State info:
            # 0: start, 255: reject, 254: accept.
            state = 0
            while state != 255 and state != 254:
                fail_count -= 1
                if fail_count == 0:
                    print("Failsafe breaking out loop!")
                    break

                try:
                    # Input the state and symbol into the machine
                    # and get resulting state, symbol, and direction.
                    machine_output = machine[(str(state), tape[tape_head])]
                except KeyError:
                    break  # Breaks if not a valid input into the dictionary.

                # Update values based on what values the machine was fed.
                state = int(machine_output[0])
                tape[tape_head] = machine_output[1]
                # Move the tape head by 1, but have it stay in bounds.
                if machine_output[2] == 'L':
                    if tape_head > 0:
                        tape_head -= 1
                else:
                    tape_head += 1
                    # If tape runs out of space, add more blank symbols.
                    if tape_head == len(tape):
                        tape.append('@0')
            if state == 254:
                accept_count += 1
                string += '\n'
                outfile.write(string)
    # After writing the txt files, write the log file.
    with open(log_directory, 'a+') as outfile:
        line = f"{machine_name},{accept_count}\n"
        outfile.write(line)
    print("Finished")


def read_machine(machine_filename):
    """
    Read a .tm file and return the machine as a dictionary.
    :param str machine_filename:
    :return: machine
    :rtype: dict
    """

    # The machine takes a state and a symbol
    # and outputs a state, symbol, and direction.
    machine = {}
    with open(machine_filename, 'r') as infile:
        for line in infile.readlines():
            # Format per line: <FromState, ReadSymbol, ToState, WriteSymbol, HeadDirection>
            line = line.strip().replace(' ', '').split(',')
            from_state = line[0]
            read_symbol = line[1]
            to_state = line[2]
            write_symbol = line[3]
            head_direction = line[4]
            machine[(from_state, read_symbol)] = (to_state, write_symbol, head_direction)
    return machine


if __name__ == "__main__":
    main()
