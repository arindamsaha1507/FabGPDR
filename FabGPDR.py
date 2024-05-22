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


def submit_job(
    config,
    script,
    label,
    wall_time="0:15:0",
    memory="4G",
    cores=1,
    **args,
):
    """Submit a job to the cluster."""
    # pylint: disable=too-many-arguments

    execute(put_configs, config)

    job(
        {
            "script": script,
            "wall_time": wall_time,
            "memory": memory,
            "cores": cores,
            "label": label,
        },
        args,
    )


@task
@load_plugin_env_vars("FabGPDR")
def gpdr(config, run_file="compare_dimension_reductions.py", **args):
    """Single run of the GPDR model."""

    update_environment(args, {"run_file": run_file, "prefix": ""})
    with_config(config)

    set_simulation_args_list(args)

    submit_job(config, "single_run", "test", **args)


@task
@load_plugin_env_vars("FabGPDR")
def gpdr_ensemble(
    config,
    ensemble_size=200,
    ensemble_parameter="seed",
    run_file="compare_dimension_reductions.py",
    **args,
):
    """Ensemble run of the GPDR model."""

    prefix = f"#$ -t 1-{ensemble_size}\n"
    update_environment(args, {"run_file": run_file, "prefix": prefix})
    with_config(config)

    set_simulation_args_list(args, {"ensemble_parameter": ensemble_parameter})

    submit_job(config, "single_run", "ensemble_test", **args)


def set_simulation_args_list(*dicts):
    """Set the simulation arguments list from the given settings."""

    for adict in dicts:

        if "ensemble_parameter" in adict:
            env.simulation_args[adict["ensemble_parameter"]] = "$SGE_TASK_ID"

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
