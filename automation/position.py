class Position:
    def __init__(self, x=0, z=0):
        """
        Initializes an instance of the class.

        Args:
            x (int): The x-coordinate of the point. Defaults to 0.
            z (int): The z-coordinate of the point. Defaults to 0.
        """
        self.x = x
        self.z = z

    def get_position(self):
        """
        Get the position of the object.

        Returns:
            Tuple: A tuple containing the x and z coordinates of the object.
        """
        return self.x, self.z
    def set_position(self, x, z):
        """
        Set the position of the object in the x and z coordinates.

        Parameters:
            x (int): The x coordinate of the object's position.
            z (int): The z coordinate of the object's position.
        """
        self.x = x
        self.z = z
    
