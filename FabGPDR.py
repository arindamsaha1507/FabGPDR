"""Module for running FabGPDR tasks."""

from fabsim.base.fab import *

# Add local script, blackbox and template path.
add_local_paths("FabGPDR")


@task
@load_plugin_env_vars("FabGPDR")
def gpdr(config, script="main.py", **args):
    """
    parameters:
      - config : [e.g. brent,harrow,ealing,hillingdon]
      - measures : name of measures input YML file
      - starting_infections : number of infections to seed 20 days prior to simulation start
      - quicktest : use larger house sizes to reduce simulation initialisation time
    """
    update_environment(args, {"script": script})
    with_config(config)
    # print(env)
    # exit()

    execute(put_configs, config)
    job(dict(script="single_run", wall_time="0:15:0", memory="4G", label="test"), args)
