from __future__ import annotations
import csv
import logging
import threading
from abc import ABC, abstractmethod
from io import StringIO
from pathlib import Path
from typing import Callable, Any

LOGDIR = Path('./logs/')

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


class Csv:
    def __init__(self, plugin:Plugin, in_file: Path, out_dir: str):
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        out_file = Path(out_dir+'/in_out.csv')
        out_file.touch()
        self.out_file = None
        self.in_file = None
        self.in_vars = ['input.' + x for x in plugin.input.__dict__]
        self.out_vars = ['output.' + x for x in plugin.output.__dict__]
        self.plugin = plugin
        if in_file:
            self.in_file = in_file
            self.in_dict: {} = list(csv.DictReader(open(in_file)))
        if out_file:
            self.out_file = out_file
            column_names = ['clock_tick']+self.in_vars+self.out_vars+['log']+[self.plugin._plugin_name]
            self.out_writer_file = open(self.out_file, 'w', newline='')
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
            if in_name.startswith('input'):
                self.plugin.input.__getattribute__(in_name.split('.')[1]) # Fails if attribut doesn't exists
                #self.plugin.__setattr__(in_name, self.str_to_nbr(value))
                e = f'self.plugin.{in_name}={value}'
                print(e)
                exec(e)

    def _compare_output_with_dict(self, row: {}):
        out_name: str
        diff = {}
        for out_name, expected  in row.items():
            if out_name.startswith('output.'):
                real = self.plugin.output.__getattribute__(out_name.split('.')[1]) # Fails if attribut doesn't exists
                if eval(str(expected)) != eval(str(real)):
                    diff.update({out_name: {'real':real, 'expected':expected}})
        return diff

    def save_output_to_file(self, clock_tick):
        if self.out_file:
            d = {}
            d.update({'clock_tick': clock_tick})
            for out_var in self.in_vars:
                d.update({out_var: eval(f'self.plugin.{out_var}')})
            for out_var in self.out_vars:
                d.update({out_var: eval(f'self.plugin.{out_var}')})
            d.update({'log':self.plugin.log_buffer.getvalue().replace('\n', '   ')})
            self.plugin.log_buffer.truncate(0)
            self.plugin.log_buffer.seek(0)
            #d.update({'log': "qwerty"})
            self.out_writer.writerow(d)
            print("QQQ", d)

    def run_test_from_file(self, verif_file: Path = None) -> []:
        print(f"{self.plugin._plugin_name} running test with data from:{verif_file}", end=' -> ')
        all_diff=[]
        verif_dict: {} = list(csv.DictReader(open(verif_file), quoting = csv.QUOTE_NONNUMERIC))
        for clock_tick, verif_data in enumerate(verif_dict):
            Plugin.clock_tick = clock_tick
            #print(f"Testing: {self.plugin.plugin_name}: {verif_data}")
            print("New clock")
            self._fetch_input_from_dict(verif_data)
            self.plugin.execute_node()
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



class Plugin(ABC):
    _execution_list: list[Plugin]
    _all_plugins: list[Plugin] = []
    api: Api
    __names = []
    clock_tick: int = 0
    running: bool
    plugin_name:str


    def __init__(self, input, output, parent:Plugin, plugin_name:str=None, csv_in: Path=None, *args, **kwargs):
        #super().__init__(*args, **kwargs)
        self._connections = []
        self.debug = {}
        self._execution_list = []
        self.api = Api()
        self.parent = parent
        self.input = input
        self.output = output
        self._plugin_name = self.get_unique_name(plugin_name)
        self.csv = Csv(self, csv_in, LOGDIR.name+'/'+self._plugin_name)
        self.running = False
        self.timeout = 0.05
        self.log = logging.getLogger(self._plugin_name)
        self.log_buffer = StringIO()
        handler = logging.StreamHandler(self.log_buffer)
        handler.setFormatter(logging.Formatter('Line:%(lineno)s-%(message)s'))
        self.log.addHandler(handler)
        logging.basicConfig(filename='logs/logger.log', level=logging.INFO,
                        format='%(asctime)s,%(msecs)d %(levelname)-5s P:%(name)s  %(message)s [%(funcName)s() %(filename)s:%(lineno)d]',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        force=True)

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

    def execute(self):
        debug = {}
        self.connect_external_inputs()
        for plugin in self._execution_list:
            #print(f"{self._plugin_name} Executing:{plugin._plugin_name}")
            d = plugin.execute()
            debug.update(d)
        print(f"{self._plugin_name} Executing_self:{self._plugin_name}")
        self.execute_self()
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

    def run_thread(self):
        self.running = True
        self.main_loop()
        self.running = False
        pass

    def execute_self(self) -> {}:
        self.debug = {}
        self.csv.fetch_input_from_in_file(Plugin.clock_tick)
        if not self.running:
            t = threading.Thread(target=self.run_thread)
            t.start()
            t.join(timeout=self.timeout)
            if t.is_alive():
                print(f"WARNING: {self._plugin_name} didn't complete")
        for connection in self._connections:
            connection()
        self.csv.save_output_to_file(Plugin.clock_tick)
        return self.debug


    def execute_node(self):
        self.run()
        self.csv.save_output_to_file(Plugin.clock_tick)
        self.run_post()

    @abstractmethod
    def run(self):
        pass

    def run_post(self):
        pass

    def main_loop(self):
        pass

    def connect_external_inputs(self):
        pass
