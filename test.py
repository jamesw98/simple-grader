class Test:
    def __init__(self, name, points, input_file, expected_output_file,
                 points_off_per_line, max_points_off, stdout, student_output, arguments, main):
        self.name = name # test name
        self.points = points # points for this test
        self.input_file = input_file # the name for the input file 
        self.expected_output_file = expected_output_file # name of the expected output file
        self.points_off_per_line = points_off_per_line # points taken off for incorrect line
        self.max_points_off = max_points_off # maximum point deduction
        self.stdout = stdout # whether or not the program writes to stdout
        self.student_output = student_output # the student output file (if not writing to stdout)
        self.arguments = arguments # the arguments for the program (if any)
        self.main = main # the main program name (for java programs given in a compressed file)