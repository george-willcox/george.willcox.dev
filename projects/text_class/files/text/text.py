# 12/11/20
# George Willcox
# Version: 3.2
# Text class

import pygame


class Text:
    # The anchor points to choose between when creating a text object
    available_anchors = ('topleft', 'bottomleft', 'topright', 'bottomright',
                         'midtop', 'midleft', 'midbottom', 'midright', 'center')
    def __init__(self, position=(0, 0), text='', colour=(0, 0, 0), size=36, font='Lucida Sans', anchor='topleft'):
        """
        Creates a mutable text object
        :param position: The position of the text
        :param text: The text to display
        :param colour: The colour of the text
        :param size: The font size
        :param font: The font to use
        :param anchor: The anchor point of the text, see `available_anchors` above.
        """
        self.position = position
        self.size = size
        self.colour = colour
        self.font = font
        self.text = str(text)
        self.anchor = anchor

        # Creates text surface
        self.font_type = pygame.font.SysFont(self.font, self.size)
        self.surface = self.font_type.render(self.text, 1, self.colour)
        self.rect = None

        # Creates rect using the anchor point. Using exec is usually ill-advised, but here it is limited to a few cases.
        if anchor in self.available_anchors:
            try:
                exec('self.rect = self.surface.get_rect(' + self.anchor + '=self.position)')
            except TypeError:
                raise Exception(f'Invalid position {self.position}')
        else:
            raise Exception(f'Invalid anchor point {self.anchor}')

    def set_text(self, *text):
        """
        Sets the text to display
        :param text: The text to display
        """
        self.text = ''

        for item in text:  # Joins all items passed with spaces
            self.text += str(item) + ' '

        self.text = self.text[:-1]  # Removes the space off the end of the string

        # Render the new text
        self.surface = self.font_type.render(self.text, 1, self.colour)

        # Get the new rect
        if anchor in self.available_anchors:
            try:
                exec('self.rect = self.surface.get_rect(' +
                     self.anchor + '=self.position)')
            except TypeError:
                raise Exception(f'Invalid position {self.position}')
        else:
            raise Exception(f'Invalid anchor point {self.anchor}')

    def update_settings(self, **settings):
        """
        Updates various setting of the text object, then renders it
        :param settings: key-word arguments for settings and their new values
        """
        self.__dict__.update(settings)

        # Creates text surface
        self.font_type = pygame.font.SysFont(self.font, self.size)
        self.surface = self.font_type.render(self.text, 1, self.colour)

        # Sets the rect
        if anchor in self.available_anchors:
            try:
                exec('self.rect = self.surface.get_rect(' + self.anchor + '=self.position)')
            except TypeError:
                raise Exception(f'Invalid position {self.position}')
        else:
            raise Exception(f'Invalid anchor point {self.anchor}')

    def draw(self, surface):
        """
        Draws the text object
        :param surface: The surface to blit the text to
        """
        surface.blit(self.surface, self.rect)


