import digitalio


class Button:
    """ Button convenience class.

    Create a button:
    >>> button = Button(board.D3, digitalio.Pull.UP)
    Update the button state:
    >>> button.update()
    And then check for conditions:
    >>> if button.pressed():
    >>>     ...
    >>> if button.just_pressed():
    >>>     ...
    >>> if button.just_released():
    >>>     ...
    """

    def __init__(self, pin, mode):
        """ Create a new Button.
        """
        self.button = digitalio.DigitalInOut(pin)
        self.button.switch_to_input(pull=mode)
        self.mode = mode
        self.last_state = False
        self.state = False

    def update(self):
        """ Read the current button state and update internal state.
        """
        # Update the last state
        self.last_state = self.state
        # Read the current state
        if self.mode == digitalio.Pull.DOWN:
            self.state = self.button.value
        elif self.mode == digitalio.Pull.UP:
            self.state = not self.button.value
        # Update the pressed / released states
        self.edge_up = self.state and not self.last_state
        self.edge_down = not self.state and self.last_state

    def pressed(self):
        """ Returns true if currently pressed.
        """
        return self.state

    def just_pressed(self):
        """ Returns true if just pressed
        True for released -> pressed transition.
        """
        return self.edge_up

    def just_released(self):
        """ Returns true if just released
        True for pressed -> released transition.
        """
        return self.edge_down
