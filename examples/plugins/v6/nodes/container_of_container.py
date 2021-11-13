import math

from examples.plugins.v6.nodes.Generator import Generator
from examples.plugins.v6.nodes.container_of_plugins import Container_of_plugins

from examples.plugins.v6 import Plugin


class Container_of_container(Plugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create nodes
        self.generator_speed = Generator(plugin_name='HeightGenerator', expression=lambda loop_index: math.cos(loop_index / 100) * 100)
        self.container_of_plugins = Container_of_plugins(plugin_name='Container_of_plugins')
        self.generator_speed.connect(self.container_of_plugins, Container_of_plugins.in_speed, Generator.out_value)

        self.add_plugin(self.generator_speed)
        self.add_plugin(self.container_of_plugins)
        self.add_plugin(self)


    def main_loop(self, loop_counter: int):
        pass
