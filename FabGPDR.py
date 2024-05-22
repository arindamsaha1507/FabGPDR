"""Module for running FabGPDR tasks."""

# pylint: disable=invalid-name

from fabsim.base.fab import (
    update_environment,
    load_plugin_env_vars,
    execute,
    job,
    task,
    with_config,
    put_configs,
    add_local_paths,
    env,
)

# Add local script, blackbox and template path.
add_local_paths("FabGPDR")


@task
@load_plugin_env_vars("FabGPDR")
def gpdr(config, script="compare_dimension_reductions.py", **args):
    """
    parameters:
      - config : [e.g. brent,harrow,ealing,hillingdon]
      - measures : name of measures input YML file
      - starting_infections : number of infections to seed 20 days prior to simulation start
      - quicktest : use larger house sizes to reduce simulation initialisation time
    """
    update_environment(args, {"script": script})
    with_config(config)

    set_simulation_args_list(args)

    execute(put_configs, config)
    job(
        {
            "script": "single_run",
            "wall_time": "0:15:0",
            "memory": "4G",
            "label": "test",
        },
        args,
    )


def set_simulation_args_list(*dicts):
    """Set the simulation arguments list from the given settings."""

    for adict in dicts:
        for key in env.simulation_args.keys():
            if key in adict:
                env.simulation_args[key] = adict[key]

    env.simulation_args_list = ""
    for key, value in env.simulation_args.items():
        if isinstance(value, (list)):
            env.simulation_args_list += "  ".join(value)
        else:
            env.simulation_args_list += f" --{key} {value}"

    print("Simulation prepared with args list:", env.simulation_args_list)
