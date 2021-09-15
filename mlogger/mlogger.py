from pathlib import Path
from functools import wraps
import json

def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


def action_decorator(function):
    def wrapper(*args,**kwargs):
        import inspect, time
        name = str(function.__name__)
        args_name = list(inspect.getfullargspec(function)[0])
        args_values = list(args)
        for i in range(len(args)):
            arg_val = args_values[i]
            if (not is_jsonable(arg_val)):
                args_values[i] = "No serializable"
        variables = dict(zip(args_name, args_values))
        t0 = time.time()
        result = function(*args)
        dt = int((time.time() - t0)*1000)/1000
        print (result)
        action = {
            "name": name,
            "value": variables,
            "duration": dt,
            "status": result["status"]
        }
        if (result["status"] > 0):
            message = result["message"]
        else:
            message = "OK"
        Logger.get_instance().info(module=name, action=action, message=message)
        return result
    return wrapper

def action_class_decorator(function):
    @wraps(function)
    def _impl(self, *args,**kwargs):
        import inspect, time
        name = str(function.__name__)
        args_name = list(inspect.getfullargspec(function)[0])
        args_values = list(args)
        for i in range(len(args)):
            arg_val = args_values[i]
            if (not is_jsonable(arg_val)):
                args_values[i] = "No serializable"
        variables = dict(zip(args_name, args_values))
        t0 = time.time()
        result = function(self, *args, **kwargs)
        dt = int((time.time() - t0)*1000)/1000
        action = {
            "name": name,
            "value": variables,
            "duration": dt,
            "statue": result["status"]
        }
        if (result["status"] > 0):
            message = result["message"]
        else:
            message = "OK"
        Logger.get_instance().info(module=name, action=action, message=message)
        return result
    return _impl

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=Singleton):
    uuid = None
    level = None
    module = None
    component = None
    path = "/home/{user}/log/{component}/"
    def __init__(self):
        pass


    def get_instance():
        return Logger()

    def configure(self, uuid, component, user):
        '''
        uuid: Nombre para identificar instancia del sistema
        component: Nombre del servicio que se esta ejecutando
        user: Nombre de usuario de quien ejecuta el proceso para escribir en su carpeta /home/{user}/log
        '''
        self.uuid = uuid
        self.component = component
        try:
            path = self.path.format(user=user, component=component)
            Path(path).mkdir(parents=True, exist_ok=True)
            self.path=path
            return 0
        except Exception as e:
            print (e)
            return 1

    def info(self, module, message=None, action=None):
        return self.__log("INFO", module, message, action)

    def warn(self, module, message=None, action=None):
        return self.__log("WARN", module, message, action)

    def error(self, module, message=None, action=None):
        return self.__log("ERROR", module, message, action)

    def verbose(self, module, message=None, action=None):
        return self.__log("VERBOSE", module, message, action)

    def critical(self, module, message=None, action=None):
        return self.__log("CRITICAL", module, message, action)

    def __get_timestamp(self):
        import time
        return int(time.time()*1000)

    def __get_log_name(self):
        from datetime import datetime 
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        uuid = self.uuid
        if (uuid is None):
            uuid= "undefined"
        log_name = "{}_{}.log".format(uuid, date)
        return log_name
    
    def __write(self, log):
        try:
            with open(self.path + self.__get_log_name(), "a+") as f:
                f.write(log)
                f.write('\n')
                return 0
        except Exception as e:
            print (e)
            return 1

    def __log(self, level, module, message, action):
        import json
        output = {
            "uuid": self.uuid,
            "ts": self.__get_timestamp(),
            "level": level,
            "module": module,
            "component": self.component,
            "message": message,
            "action": action
        }
        output = {k: v for k, v in output.items() if v is not None}
        try:
            log = json.dumps(output, indent=0)
            log = "".join(log.split('\n'))
            log = "'".join(log.split('"'))
            self.__write(log)           
        except Exception as e:
            pass



