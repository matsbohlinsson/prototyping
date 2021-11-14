import math

from examples.plugins.v6.nodes.Generator import Generator
from examples.plugins.v6.nodes.container_of_plugins import Container_of_plugins
from examples.plugins.v6 import OutSpeed, InSpeed, Plugin

from examples.plugins.v6 import Plugin


class Container_of_container(Plugin, InSpeed, OutSpeed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create nodes
        self.container_of_plugins = Container_of_plugins(parent=self, plugin_name='Container_of_plugins')

        self.add_plugin(self.container_of_plugins)
        #self.add_plugin(self)
        self.container_of_plugins.connect(self, Container_of_container.out_speed, Container_of_plugins.out_speed)


    def main_loop(self):
        pass

    def connect_external_inputs(self):
        self.container_of_plugins.in_speed = self.in_speed
