class Test:
    def __init__(self, name, points, input_file, expected_output_file,
                 points_off_per_line, max_points_off, stdout, student_output):
        self.name = name
        self.points = points
        self.input_file = input_file
        self.expected_output_file = expected_output_file
        self.points_off_per_line = points_off_per_line
        self.max_points_off = max_points_off
        self.stdout = stdout
        self.student_output = student_output