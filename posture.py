# slouch_detector/posture.py

"""
Tracks current key_point coordinates and uses these to check for
various improper postures.
Stores a scale factor, which is used to reduce or increase the distances
that are used to calculate distance between key_points to determine if
improper posture is detected.
Posture is measured with these individual functions in order to allow users to
check for specific bad behavior,
"""
class CheckPosture:

    def __init__(self, scale=1, key_points={}):
        self.key_points = key_points
        self.scale = scale
        self.message = ""

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
        if self.key_points['Left Shoulder'].x != -1 and self.key_points['Left Ear'].x != -1 \
            and  self.key_points['Left Shoulder'].x >= (self.key_points['Left Ear'].x + (self.scale * 180)):
                return False
        if self.key_points['Right Shoulder'].x != -1 and self.key_points['Right Ear'].x != -1 \
            and  self.key_points['Right Shoulder'].x >= (self.key_points['Right Ear'].x + (self.scale * 180)):
                return False

        return True


    def check_slump(self):
        """
        Checks whether a uses is slumped down in their chair (shoulders at eye level)
        :return: Boolean
            True if not slumped; False if slumped
        """
        if self.key_points['Neck'].y != -1 and self.key_points['Nose'].y != -1 \
            and (self.key_points['Nose'].y >= self.key_points['Neck'].y - (self.scale * 150)):
            return False
        return True


    def check_head_drop(self):
        """
        Checks whether a use has tilted their head downwards, chin towards chest (eyes are at ear level)
        :return: Boolean
            True if not head not tilted downwards; False if tilted downward
        """
        if self.key_points['Left Eye'].y != -1 and self.key_points['Left Ear'].y != -1 \
            and self.key_points['Left Eye'].y > (self.key_points['Left Ear'].y + (self.scale * 10)):
                return False
        if self.key_points['Right Eye'].y != -1 and self.key_points['Right Ear'].y != -1 \
            and self.key_points['Right Eye'].y > (self.key_points['Right Ear'].y + (self.scale * 10)) :
                return False
                        
        return True

    def correct_posture(self):
        """
        Checks all current posture functions
        :return: Boolean
            True if all posture functions return True; False otherwise
        """
        return all([self.check_slump(), self.check_head_drop(), self.check_lean_forward()])