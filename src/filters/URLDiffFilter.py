class URLDiffFilter:
    """ The URLDiffFilter checks for the amount of differing characters in the
        URLs passed into the is_filtered function. If the difference of characters in
        the URL is less than or equal to the acceptable_diff a tolerance amount of times,
        it will be filtered.
    """

    def __init__(self, tolerance=25, acceptable_diff=3):
        self.tolerance = tolerance
        self.acceptable_diff = acceptable_diff
        self.flags = 0
        self.previous_url = ""

    def is_filtered(self, p_url):
        url = p_url.get_url(trim_parameters=True)
        if self.diff(url, self.previous_url) <= self.acceptable_diff:
            self.flags += 1
        else:
            self.flags = 0
        self.previous_url = url
        return self.flags >= self.tolerance

    """
        Returns the number of out-of-place characters between two strings
        characters in a string.
        Ex:
            "Hello, world!"
            "hello world!"
             ^    ^^^^^^^^
        Would return 9
    """
    @staticmethod
    def diff(str1, str2):
        diffs = 0
        for pair in zip(str1, str2):
            if pair[0] != pair[1]:
                diffs += 1
        return diffs + abs(len(str1) - len(str2))
