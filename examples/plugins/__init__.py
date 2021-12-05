from examples.plugins.v6 import Plugin


class GeneralPlugin(Plugin):
    def __init__(self, input, output, run_function, run_post_function, plugin_name, parent, *args, **kwargs):
        self.input=input
        self.output=output
        self.run_function=run_function
        self.run_post_function=run_post_function
        super().__init__(input=input, output=output, parent=parent, plugin_name=plugin_name, *args, **kwargs)

    def run(self):
        self.run_function(self.input, self.output, self.log)

    def run_post(self):
        self.run_post_function(self.input, self.output, self.log)