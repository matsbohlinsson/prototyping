from __future__ import annotations
import csv
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Any

LOGDIR = Path('./csv_out/')

class Interface:
    _observers: []
    def __init__(self, *args, **kwargs):
        self._observers = []
        pass

    def _value_changed(self, old, new):
        if old != new:
            for callback in self._observers:
                callback(new)

class Interface_in(Interface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Interface_out(Interface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Ispeed(Interface_in):
    pass


class P:
    def __init__(self, value):
        super().__init__()
        self._value = value

    def set(self, value):
        self._value = value

    def get(self):
        return self._value


class OutValue(Interface_out):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._out_value = 0

    @property
    def out_value(self):
        return self._out_value

    @out_value.setter
    def out_value(self, value):
        self._out_value = value


class OutSpeed(Interface_out):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._out_speed = 0

    @property
    def out_speed(self):
        return self._out_speed

    @out_speed.setter
    def out_speed(self, speed):
        self._out_speed = speed


class InSpeed(Interface_in):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._in_speed = 0

    @property
    def in_speed(self):
        return self._in_speed

    @in_speed.setter
    def in_speed(self, speed):
        self._in_speed = speed

class InDeltaMax(Interface_in):
    def __init__(self, in_delta_max=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.in_delta_max = in_delta_max

    @property
    def in_speed(self):
        return self._in_speed

    @in_speed.setter
    def in_speed(self, speed):
        self._in_speed = speed

class InHeight(Interface_in):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._in_height = 0

    @property
    def in_height(self):
        return self._in_height

    @in_height.setter
    def in_height(self, height):
        self._in_height = height

class InCourse(Interface_in):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course = None

class InWindowSize(Interface_in):
    def __init__(self, in_window_size:int=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._in_window_size = in_window_size

    @property
    def in_window_size(self):
        return self._in_window_size

    @in_window_size.setter
    def in_window_size(self, new):
        old = self._in_window_size
        self._in_window_size = new
        self._value_changed(old, new)

    def onchange_in_window_size(self, callback):
        self._observers.append(callback)


class OutCourse(Interface_in):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course = None


class OutHeight(Interface_in):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.out_height = None
    @property
    def out_height(self, *args, **kwargs):
        return self._out_height

    @out_height.setter
    def out_height(self, height, *args, **kwargs):
        self._out_height = height


class OutLatLon(Interface_in):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.out_lat = None
        self.out_lon = None


class InLatLon(Interface_in):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.in_lat = None
        self.in_lon = None


class Runtime():
    def __init__(self):
        pass

    def sleep(self):
        pass

    def sleep_until_next_execution(self):
        pass

    def wait(self, lambda_expression):
        while not lambda_expression():
            self.sleep_until_next_execution()


class Dji():
    def __init__(self, runtime):
        self.runtime=runtime
        pass

    def takeoff(self):
        #print("Taking off")
        #self.java.takeoff()
        self.runtime.wait(lambda: self.is_flying())

    def is_flying(self):
        return True


class Api:
    def __init__(self):
        self.runtime = Runtime()
        self.dji = Dji(self.runtime)


class Plugin(ABC):
    _execution_list: list[Plugin]
    _all_plugins: list[Plugin] = []
    api: Api
    __names = []

    class Csv:
        def __init__(self, plugin:Plugin, in_file: Path, out_dir: Path):
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = Path(out_dir.name+'/in_out.csv')
            self.out_file = None
            self.in_file = None
            self.in_vars = [attr for attr in dir(plugin) if attr.startswith('in_')]
            self.out_vars = [attr for attr in dir(plugin) if attr.startswith('out_')]
            self.plugin = plugin
            if in_file:
                self.in_file = in_file
                self.in_dict: {} = list(csv.DictReader(open(in_file)))
            if out_file:
                self.out_file = out_file
                column_names = ['loop_counter']+self.in_vars+self.out_vars+[self.plugin._plugin_name]
                self.out_writer_file = open(self.out_file, 'w')
                self.out_writer = csv.DictWriter(self.out_writer_file, fieldnames=column_names, quoting = csv.QUOTE_NONNUMERIC)
                self.out_writer.writeheader()


        def str_to_nbr(self, string):
            try:    return float(string)
            except:  return string

        def fetch_input_from_in_file(self, row_nbr: int):
            if self.in_file:
                self._fetch_input_from_dict(self.in_dict[row_nbr])

        def _fetch_input_from_dict(self, row: {}):
            in_name: str
            for in_name, value  in row.items():
                if in_name.startswith('in_'):
                    self.plugin.__getattribute__(in_name) # Fails if attribut doesn't exists
                    self.plugin.__setattr__(in_name, self.str_to_nbr(value))

        def _compare_output_with_dict(self, row: {}):
            out_name: str
            diff = {}
            for out_name, expected  in row.items():
                if out_name.startswith('out_'):
                    real = self.plugin.__getattribute__(out_name) # Fails if attribut doesn't exists
                    if expected != real:
                        diff.update({out_name: {'real':real, 'expected':expected}})
            return diff

        def save_output_to_file(self, loop_counter: int):
            if self.out_file:
                d = {}
                d.update({'loop_counter': loop_counter})
                for out_var in self.in_vars + self.out_vars:
                    d.update({out_var: self.plugin.__getattribute__(out_var)})
                self.out_writer.writerow(d)

        def run_test_from_file(self, verif_file: Path = None) -> []:
            print(f"{self.plugin._plugin_name} running test with data from:{verif_file}", end=' -> ')
            all_diff=[]
            verif_dict: {} = list(csv.DictReader(open(verif_file), quoting = csv.QUOTE_NONNUMERIC))
            for loop_nbr, verif_data in enumerate(verif_dict):
                #print(f"Testing: {self.plugin.plugin_name}: {verif_data}")
                print("New clock")
                self._fetch_input_from_dict(verif_data)
                self.plugin.execute(loop_nbr)
                diff = self._compare_output_with_dict(verif_data)
                if diff:
                    all_diff.append(diff)
                    print("Diff:", diff)
            if all_diff or len(verif_dict)<10:
                print(f'FAILED:{len(all_diff)} rows')
            else:
                print(f"SUCCESS {len(verif_dict)} rows")
            return all_diff

        def __del__(self):
            self.out_writer_file.close()
            pass


    def __init__(self, parent:Plugin, plugin_name:str=None, csv_in: Path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._connections = []
        self.debug = {}
        self._execution_list = []
        self.api = Api()
        self.parent = parent
        self._plugin_name = self.get_unique_name(plugin_name)
        self.csv = Plugin.Csv(self, csv_in, Path(LOGDIR.name+'/'+self._plugin_name))

    def get_unique_name(self, plugin_name):
        name = self.__class__.__name__ if plugin_name is None else plugin_name
        if name in Plugin.__names:
            name_orig = name
            i=0
            while name in Plugin.__names:
                i=i+1
                name = name_orig + f'_{i}'
            Plugin.__names.append(name)
        if self.parent is not None:
            name = f'{self.parent._plugin_name}/{name}'
        return name


    def add_plugin(self, plugin: Plugin):
        self._execution_list.append(plugin)
        Plugin._all_plugins.append(plugin)

    def execute(self, loop_counter: int):
        debug = {}
        self.connect_external_inputs()
        for plugin in self._execution_list:
            print(f"Executing:{plugin._plugin_name}")
            #d = plugin.main_execution(loop_counter)
            d = plugin.execute(loop_counter)
            debug.update(d)
        print(f"Executing:{self._plugin_name}")
        self.execute_self(loop_counter)
        return debug

    def _connect(self, inp_obj: Plugin, out: Callable[[Any], Any], inp: Callable[[Any], Any]):
        def debug_info(connection_name:str, value):
            self.debug.update({connection_name: value})

        def transfer(out, out_obj, inp, inp_obj):
            inp(inp_obj, out(out_obj))
            debug_info(f'{out_obj._plugin_name}.{out.__name__}', out(out_obj))
            debug_info(f'{inp_obj._plugin_name}.{inp.__name__}', out(out_obj))

        out_obj = self
        #print(out, out_obj, inp, inp_obj)
        self._connections.append(lambda out=out, out_obj=out_obj, inp=inp, inp_obj=inp_obj: transfer(out, out_obj, inp, inp_obj))

    def connect(self, inp_obj: Plugin, inp, out):
        self._connect(inp_obj, out.fget, inp.fset)

    def execute_self(self, loop_counter: int) -> {}:
        self.debug = {}
        self.csv.fetch_input_from_in_file(loop_counter)
        self.main_loop(loop_counter)
        for connection in self._connections:
            connection()
        self.csv.save_output_to_file(loop_counter)
        return self.debug

    @abstractmethod
    def main_loop(self, loop_counter: int):
        pass

    def connect_external_inputs(self):
        pass