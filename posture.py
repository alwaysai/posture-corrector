# slouch_detector/posture.py

"""
Tracks current key_point coordinates and uses these to check for
various improper postures.
Stores a scale factor, which is used to reduce or increase the distances
that are used to calculate distance between key_points to determine if
improper posture is detected.
Posture is measured with these individual functions in order to allow users to
check for specific bad behavior.
"""
class CheckPosture:

    def __init__(self, scale=1, key_points={}):
        self.key_points = key_points
        # set scale > 1 for more relaxed posture detection
        self.scale = scale
        self.message = ""
        # set data to be a dictionary containing empty
        # lists for keypoints and lines showing poor posture
        self.data = {}
        self.new_data()

    def new_data(self):
        """
        Helper function to re-set the data (the 'bad' posture
        points and lines) to be an empty dictionary.
        """
        self.data = {
            "lines": [],
            "points": []
        }

    def set_key_points(self, key_points):
        """
        Updates the key_points dictionary used in posture calculations
        :param key_points: {}
            the dictionary to use for key_points
        """
        self.key_points = key_points

    def get_key_points(self):
        """
        Returns the instance's current version of the key_points dictionary
        :return: {}
            the current key_points dictionary
        """
        return self.key_points

    def set_message(self, message):
        """
        Setter to update the message manually if needed
        :param message: string
            The message to override the current message
        """
        self.message = message

    def build_message(self):
        """
        Builds a string with advice to the user on how to correct their posture
        :return: string
            The string containing specific advice
        """
        current_message = ""
        if not self.check_head_drop():
            current_message += "Lift up your head!\n"
        if not self.check_lean_forward():
            current_message += "Lean back!\n"
        if not self.check_slump():
            current_message += "Sit up in your chair, you're slumping!\n"
        self.message = current_message
        return current_message

    def get_message(self):
        """
        Getter method to return the current message
        :return: string
            The current posture message
        """
        return self.message

    def get_data(self):
        """
        Getter method to return latest 'bad' posture points
        :return: dictionary containing 'points' and 'lines',
        which connect the points
        """
        self.new_data()
        self.correct_posture()
        return self.data

    def set_scale(self, scale):
        """
        Sets the scale factor to use for the posture calculations
        :param scale: int
            The value to scale the measurements used in the calculations by. Larger values will
            mean a less stringent calculation.
        """
        self.scale = scale

    def get_scale(self):
        """
        Returns the current scale for the instance
        :return: int
            The scale being used by the instance for posture calculations
        """
        return self.scale

    def check_lean_forward(self):
        """
        Checks whether an individual is leaning forward (head towards computer screen)
        :return: Boolean
            True if not leaning forward; False otherwise
        """
        x1 = self.key_points['Left Shoulder'].x
        x2 = self.key_points['Left Ear'].x
        x3 = self.key_points['Right Shoulder'].x
        x4 = self.key_points['Right Ear'].x
        y1 = self.key_points['Left Shoulder'].y
        y2 = self.key_points['Left Ear'].y
        y3 = self.key_points['Right Shoulder'].y
        y4 = self.key_points['Right Ear'].y
        if x1 != -1 and x2 != -1 \
            and x1 >= (x2 + (self.scale * 180)):
                self.data["points"].append([x1, y1])
                self.data["points"].append([x2, y2])
                self.data["lines"].append([x1, y1, x2, y2])
                return False
        if x3 != -1 and x4 != -1 \
            and x3 >= (x4 + (self.scale * 180)):
                self.data["points"].append([x3, y3])
                self.data["points"].append([x4, y4])
                self.data["lines"].append([x3, y3, x4, y4])
                return False
        return True


    def check_slump(self):
        """
        Checks whether a uses is slumped down in their chair (shoulders at eye level)
        :return: Boolean
            True if not slumped; False if slumped
        """
        x1 = self.key_points['Neck'].x
        x2 = self.key_points['Nose'].x
        y1 = self.key_points['Neck'].y
        y2 = self.key_points['Nose'].y
        if y1 != -1 and y2 != -1 \
            and y2 >= (y1 - (self.scale * 150)):
            self.data["points"].append([x1, y1])
            self.data["points"].append([x2, y2])
            self.data["lines"].append([x1, y1, x2, y2])
            return False
        return True


    def check_head_drop(self):
        """
        Checks whether a use has tilted their head downwards, chin towards chest (eyes are at ear level)
        :return: Boolean
            True if not head not tilted downwards; False if tilted downward
        """
        x1 = self.key_points['Left Eye'].x
        x2 = self.key_points['Left Ear'].x
        x3 = self.key_points['Right Eye'].x
        x4 = self.key_points['Right Ear'].x
        y1 = self.key_points['Left Eye'].y
        y2 = self.key_points['Left Ear'].y
        y3 = self.key_points['Right Eye'].y
        y4 = self.key_points['Right Ear'].y
        if y1 != -1 and y2 != -1 \
            and y1 > (y2 + (self.scale * 10)):
                self.data["points"].append([x1, y1])
                self.data["points"].append([x2, y2])
                self.data["lines"].append([x1, y1, x2, y2])
                return False
        if y3 != -1 and y4 != -1 \
            and y3 > (y4 + (self.scale * 10)):
                self.data["points"].append([x3, y3])
                self.data["points"].append([x4, y4])
                self.data["lines"].append([x3, y3, x4, y4])
                return False
                        
        return True

    def correct_posture(self):
        """
        Checks all current posture functions
        :return: Boolean
            True if all posture functions return True; False otherwise
        """
        return all([self.check_slump(), self.check_head_drop(), self.check_lean_forward()])