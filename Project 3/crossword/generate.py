import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()

        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            words = list(self.domains[var])
            for word in words:
                if len(word) != var.length:
                    self.domains[var].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False

        if not self.crossword.overlaps[x, y]:
            return revised

        i, j = self.crossword.overlaps[x, y]
        x_words = list(self.domains[x])
        for x_word in x_words:

            if not any(x_word[i] == y_word[j] for y_word in self.domains[y]):
                self.domains[x].remove(x_word)
                revised = True


        return revised



    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = arcs if arcs != None else [pair for pair in self.crossword.overlaps]
        while len(queue) > 0:
            (x, y) = queue.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in (self.crossword.neighbors(x) - {y}):
                    if (z, x) not in queue:
                        queue.append((z, x))
        return True



    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return (all(var in assignment for var in self.crossword.variables) and all(value for value in assignment.values()))

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        assignment_copy = assignment.copy()
        for v1 in assignment_copy:
            for v2 in self.crossword.neighbors(v1):
                if v2 in assignment_copy:
                    i, j = self.crossword.overlaps[v1, v2]
                    if assignment_copy[v1][i] != assignment_copy[v2][j]:
                        return False

            for v2 in assignment_copy:
                if v1 == v2:
                    continue
                if assignment_copy[v1] == assignment_copy[v2]:
                    return False
            

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        overlaps_dict = dict()

        for word in self.domains[var]:
            overlaps_num = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    continue
                if word in self.domains[neighbor]:
                    overlaps_num += 1
            overlaps_dict[word] = overlaps_num

        sorted_list = sorted(overlaps_dict.items(), key=lambda item: item[1])
        sorted_domain = [x for (x, y) in sorted_list]

        return sorted_domain

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unsorted_dict = dict()
        for var in self.crossword.variables:
            if var not in assignment:
                unsorted_dict[var] = len(self.domains[var])
        
        sorted_dict = dict(sorted(unsorted_dict.items(), key=lambda item: item[1]))

        first = list(sorted_dict.values())[0]
        sort_to_degree = dict()
        for var in sorted_dict:
            if sorted_dict[var] == first:
                sort_to_degree[var] = len(self.crossword.neighbors(var))

        sorted_degrees = sorted(sort_to_degree.items(), key=lambda item: item[1])
        sorted_degrees.reverse()

        return sorted_degrees[0][0]

    def inference(self, x):
        """
        Makes inferences (new assignments) after altering domains on
        neighbors of a variable x.
        """ 
        arcs = list()
        for neighbor in self.crossword.neighbors(x):
            arcs.append((x, neighbor))

        if self.ac3(arcs):
            inferences = dict()
            for var in self.domains:
                if len(self.domains[var]) == 1:
                    inferences[var] = list(self.domains[var])[0]
            return inferences

        else:
            return None


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            inferences = None

            if self.consistent(assignment):
                inferences = self.inference(var)
                if inferences:
                    for inference in inferences:
                        assignment[inference] = inferences[inference]
                result = self.backtrack(assignment)
                if result:
                    return result
          
            if inferences:
                for inference in inferences:
                    assignment.pop(inference)
            
            assignment.pop(var)

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
