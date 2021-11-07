import pygame
import pygame_gui


class Page:
    """ All the pygame pages in the program """

    def __init__(self, title, width, height, is_resizable=False):
        self.__title = title
        self.__width = width
        self.__height = height
        if is_resizable:
            self.__window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        else:
            self.__window = pygame.display.set_mode((width, height))

    def get_title(self):
        return self.__title

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_window(self):
        return self.__window

    def close(self):
        pygame.quit()


class GuiPage(Page):
    """ pygame_gui pages """

    def __init__(self, title, width, height, hex_color, theme=None):
        super().__init__(title, width, height)
        self.__background_color = hex_color
        pygame.display.set_caption(title)
        self.background = pygame.Surface((width, height))
        self.background.fill(pygame.Color(hex_color))
        self.theme = theme
        if self.theme is None:
            print("theme was none ...")
            self.manager = pygame_gui.UIManager((width, height))
        else:
            print("created with theme attached ! ")
            self.manager = pygame_gui.UIManager((width, height), self.theme)
        self.buttons, self.labels, self.sliders, self.textboxes, self.colorpickers = [], [], [], [], []
        self.entry_boxes, self.options_lists, self.images, self.popups = [], [], [], []
        self.clock = pygame.time.Clock()
        self.theme = theme

    # *****************************  ADDING METHODS - ADDING GUI WIDGETS  *******************************************
    def add_button(self, x=0, y=0, width=150, height=75, text="", centered=False, visible=True, object_id=None):
        """ adding a button to the Gui Page """
        if object_id is None:
            object_id = f"label{len(self.labels)}"
        if centered:
            x = self.get_window().get_width() / 2 - width / 2
        new_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x, y), (width, height)),
                                                  text=text,
                                                  manager=self.manager, visible=True, object_id=object_id)
        self.buttons.append(new_button)
        return new_button

    def add_label(self, x=0, y=0, x1=150, y1=50, text="", centered=False, visible=True, object_id=None,
                  label_object=None):
        if label_object is None:
            if object_id is None:
                object_id = f"label{len(self.labels)}"
            if centered:
                x = self.get_width() / 2 - x1 / 2
            label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((x, y), (x1, y1)),
                                                text=text,
                                                manager=self.manager, visible=True, object_id=object_id)

            self.labels.append(label)
            return label
        else:
            self.labels.append(label_object)
            return label_object

    def add_slider(self, x=0, y=0, width=150, height=30, min_value=0, max_value=100, start_value=0, centered=False,
                   visible=True):
        if centered:
            x = self.get_width() / 2 - width / 2
        new_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((x, y), (width, height)),
                                                            start_value=start_value,
                                                            value_range=(min_value, max_value),
                                                            manager=self.manager, visible=visible)
        self.sliders.append(new_slider)
        return new_slider

    def add_color_picker(self, visible=True):
        color_picker = pygame_gui.windows.UIColourPickerDialog(rect=pygame.Rect(100, 100, 390, 390),
                                                               manager=self.manager, visible=visible)
        self.colorpickers.append(color_picker)
        return color_picker

    def add_text_box(self, x=0, y=0, x1=200, y1=150, text="Add Text To This Text Box", body_color=None, centered=False,
                     visible=True):
        if centered:
            x = self.get_width() / 2 - x1 / 2
        if body_color is None:
            textbox = pygame_gui.elements.UITextBox(html_text=f"{text}",
                                                    relative_rect=pygame.Rect((x, y), (x1, y1)), manager=self.manager)
        else:

            textbox = pygame_gui.elements.UITextBox(html_text=f"<body bgcolor={body_color}>{text}</body>",
                                                    relative_rect=pygame.Rect((x, y), (x1, y1)),
                                                    manager=self.manager, visible=visible)
        self.textboxes.append(textbox)
        return textbox

    def add_entry_box(self, x=0, y=0, width=200, height=100, centered=False, visible=True):
        if centered:
            x = self.get_window().get_width() / 2 - width / 2
        text_entry = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=pygame.Rect((x, y), (width, height)), manager=self.manager, visible=visible)
        self.entry_boxes.append(text_entry)
        return text_entry

    def add_options_list(self, options_list, starting_position, x=0, y=0, width=150, height=50, centered=False,
                         visible=True):
        if centered:
            x = self.get_width() / 2 - width / 2
        options_list = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=options_list,
                                                                            starting_option=starting_position,
                                                                            relative_rect=pygame.Rect((x, y),
                                                                                                      (width, height)),
                                                                            manager=self.manager, visible=visible)
        self.options_lists.append(options_list)
        return options_list

    def add_image(self, path, x=0, y=0, size_factor=1, centered=False, visible=True):
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (int(img.get_width() * size_factor), int(img.get_height() * size_factor)))
        image = pygame_gui.elements.ui_image.UIImage(
            relative_rect=pygame.Rect((x, y), (img.get_width(), img.get_height())),
            image_surface=img, manager=self.manager, visible=True)
        self.images.append(image)
        return image

    def add_image_from_object(self, image_obj, x=0, y=0):
        image = pygame_gui.elements.ui_image.UIImage(
            relative_rect=pygame.Rect((x, y), (image_obj.get_width(), image_obj.get_height())),
            image_surface=image_obj, manager=self.manager, visible=True)
        self.images.append(image)
        return image

    def add_popup(self, x=0, y=0, width=200, height=200, html_message="", title="Important Message!", centered_x=False
                  , centered_y=False, visible=True):
        if centered_x:
            x = self.get_width() / 2 - width / 2
        if centered_y:
            y = self.get_height() / 2 - height / 2
        pop_up = pygame_gui.windows.ui_message_window.UIMessageWindow(rect=pygame.Rect((x, y), (width, height)),
                                                                      html_message=html_message, manager=self.manager,
                                                                      window_title=title, visible=visible
                                                                      )
        self.popups.append(pop_up)
        return pop_up

    # **************************  CLEARING - DELETING GUI OBJECTS FROM THE SCREEN  *************************************
    def clear_labels(self):
        for label in self.labels:
            label.kill()

    def clear_buttons(self):
        for button in self.buttons:
            button.kill()

    def clear_textboxes(self):
        for textbox in self.textboxes:
            textbox.kill()

    def clear_entry_boxes(self):
        for entry_box in self.entry_boxes:
            entry_box.kill()

    def clear_options_lists(self):
        for options_list in self.options_lists:
            options_list.kill()

    def clear_color_pickers(self):
        for color_picker in self.colorpickers:
            color_picker.kill()

    def clear_images(self):
        for image in self.images:
            image.kill()

    def clear_sliders(self):
        for slider in self.sliders:
            slider.kill()

    def clear_all(self):
        self.clear_labels()
        self.clear_buttons()
        self.clear_textboxes()
        self.clear_entry_boxes()
        self.clear_color_pickers()
        self.clear_sliders()
        self.clear_options_lists()
        self.clear_images()

    def animate_text_box(self, textbox, animation_type):
        if animation_type == "typing":
            textbox.set_active_effect("typing_appear")
        elif animation_type == "fade_out":
            textbox.set_active_effect("fade_out")

    def refresh(self):
        self.get_window().blit(self.background, (0, 0))

    def preview(self):
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        pass

                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.get_window().blit(self.background, (0, 0))
            self.manager.draw_ui(self.get_window())
            pygame.display.update()
