import pygame


def create_font_texture(my_string, font):
    text_surface = font.render(my_string, True, (255, 255, 255), (0, 0, 0))
    text_width, text_height = text_surface.get_size()
    text_pixels = pygame.image.tostring(text_surface, 'RGB')
    return (text_width, text_height), 3, text_pixels
    # text_texture = ctx.texture(size=(text_width, text_height), components=3, data=text_pixels)
    # text_texture.use(0)












