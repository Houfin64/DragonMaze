class Item:
    def __init__(self, use_function=None, targeting=False, arrow_targeting = False, targeting_message=None, sound=0, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.arrow_targeting = arrow_targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs
        self.sound = sound
