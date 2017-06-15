#!env/bin/python
from flask import Flask, make_response, jsonify, redirect
import psutil

app = Flask(__name__)


@app.route('/')
def index():
    times = psutil.cpu_times()
    stats = psutil.cpu_stats()
    virtual = psutil.virtual_memory()
    swap = psutil.swap_memory()

    info = {
        'cpu' : {
            'number': psutil.cpu_count(),
            'times': {
                'user': times.user,
                'system': times.system,
                'idle': times.idle
            },
            'percent': psutil.cpu_percent(percpu=True),
            'stats': {
                'ctx_switches': stats.ctx_switches,
                'interrupts':stats.interrupts,
                'soft_interrupts': stats.soft_interrupts,
                'syscalls': stats.syscalls
            }
        },
        'memory': {
            'virtual': {
                'total': virtual.total,
                'available': virtual.available,
                'percent': virtual.percent,
                'used': virtual.used,
                'free': virtual.free,
                'active': virtual.active,
                'inactive': virtual.inactive,
            },
            'swap': {
                'total': swap.total,
                'used': swap.used,
                'free': swap.free,
                'percent': swap.percent,
                'in': swap.sin,
                'out': swap.sout
            }
        },
        'network': {

        },
        'boot_time': psutil.boot_time()
    }

    return jsonify(info)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)