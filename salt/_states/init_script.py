import subprocess
import salt.loader

def get_init_system():
    """ Return the name of the init system running on the machine.

    The current default is to assume sysvinit, but will also detect upstart.
    """
    init_system = subprocess.check_output('ps aux | grep -o "[u]pstart" -m 1 || echo sysvinit', shell=True)
    return init_system.strip()


def managed(name, **kwargs):
    """ Make sure an init script is present. Set the name of the service, and a file
    source for each of the different init systems you want to support.
    """
    __states__ = salt.loader.states(__opts__, __salt__)
    __states__['file.managed'].func_globals['__env__'] = __env__
    ret = {'name': name, 'changes': {}, 'result': False, 'comment': ''}
    init_system = get_init_system()

    args = {}
    if init_system == 'upstart':
        args['name'] = '/etc/init/%s.conf' % name
        args['mode'] = '0644'
    elif init_system == 'sysvinit':
        args['name'] = '/etc/init.d/%s' % name
        args['mode'] = '0755'

    if init_system in kwargs:
        args['source'] = kwargs[init_system]
        file_ret = __states__['file.managed'](**args)
        ret['comment'] = file_ret['comment']
        ret['result'] = file_ret['result']
        ret['changes'] = file_ret['changes']
    else:
        ret['comment'] = 'No source file for present init system given: %s' % init_system
    return ret
