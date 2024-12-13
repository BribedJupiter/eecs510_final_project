# Read a file line-by-line and output the resulting array
# where each element in that array is a line
def read_file(filename):
    array = []
    f = open(filename)
    for line in f:
        l = line.split()
        array.append(l)
    f.close()
    return array

# Using the format we defined in Step 4, 
# check if the string is valid.
def check_valid_string_PDA(PDA, string):
    steps = [] # steps taken when processing each char
    current_state = None # What state are we in?
    stack = [] # What's on the stack?
    results = ["accept", "reject"]

    # Process:
    # Look at string character by character
    # - Is it a valid input character?
    # - What state are we in? 
    # - Is there a transition from our state?
    # - Can we take that transition given the stack?
    # - Take transition, update state, stack
    # On last character: 
    # - Are we in an accepting state?
    # - Is the stack empty?
    for i in range(len(string) + 1):
        # Check state. If this is the first char processed,
        # go to the start state.
        if i == 0:
            current_state = PDA[3][0]
        # If our state is not defined now, throw an error.
        if current_state is None:
            raise RuntimeError(f"Current state ({current_state}) undefined")
        # If we have processed the whole string (i == len(string))
        # then we are done and need to check if we're in an accepting state.
        if i == len(string):
            # Accept if we're in an accepting state and stack is empty
            if current_state in PDA[4] and len(stack) <= 0:
                out(results[0], steps)
            # Reject otherwise
            else:
                out(results[1])
            return # Ya ha acabado
                
        # Check valid character
        if string[i] not in PDA[1]:
            out(results[1]) # reject
            return
        
        # Check for possible transitions
        transition_options = []
        for j in range(5, len(PDA)):
            # Each line is a transition
            transition = PDA[j]
            # Ignore transitions that don't start from the current state
            if transition[0] != current_state:
                continue
            # Ignore transitions that aren't processing the current input char
            if transition[1] != string[i]:
                continue
            # If the stack is empty and we're required to pop a value, then ignore
            if transition[3] != '_' and len(stack) <= 0:
                continue
            # At this point, we have a valid transition
            transition_options.append(transition)

        # If we don't have any possible transitions, we know the string is invalid
        if len(transition_options) <= 0:
            out(results[1])
            return
        
        # Now that we have possible transitions, let's take one
        # To decide what to take:
        # - If the stack is not empty, take the first option that involves a pop
        # - Otherwise, take the first option. Usually there will only be one anyway.
        # To take:
        # - push / pop what's needed
        # - update steps
        # - update current_state
    
        # Decide on a transition:
        transition_choice = transition_options[0]
        if len(stack) > 0:
            for j in range(len(transition_options)):
                # Check if the transition is popping something
                if transition_options[j][3] != '_':
                    transition_choice = transition_options[j]
                    break # Take the first find
                
        # Pop from stack if needed
        if transition_choice[3] != '_':
            if len(stack) > 0:
                # Find the last symbol in stack that matches our symbol to pop
                index = None # index of the value we want to pop
                for k in range(len(stack)):
                    # Iterate through stack and update index as find occurrences
                    if stack[k] == transition_choice[3]:
                        index = k
                # If we don't find an occurrence of our stack symbol, something has gone wrong
                if index is None:
                    raise RuntimeError(f"{transition_choice[3]} not found on stack")
                # At this point, we have found the index of the symbol we want to remove
                # from the stack
                stack.pop(index)
            else:
                # If we want to pop but stack is empty, raise an error
                raise RuntimeError("Attempting to pop from empty stack")
        
        # Push to stack if required
        if transition_choice[4] != '_':
            stack.append(transition_choice[4])
        
        # Update steps with a tuple of info
        # Format: start_state input end_state (pop) (push)
        steps.append((current_state, transition_choice[1], transition_choice[2], transition_choice[3], transition_choice[4]))

        # Take the transition
        current_state = transition_choice[2] # Update current state


# For easier output
def out(message, steps=None):
    if steps is not None:
        print(message)
        for step in steps:
            print (step)
    else:
        print(message)

# Run the program!
def main():     
    # Read our automaton from file
    machine = read_file("automaton.txt")
    string = input("Enter the string to be checked: ")
    
    # Check if it accepts a string
    try: 
        check_valid_string_PDA(machine, string)
    except Exception as e:
        print("Error processing string. Please check input file automaton.txt")
        print("Error:", e)

if __name__ == "__main__":
    main()