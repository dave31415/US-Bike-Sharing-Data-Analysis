import cProfile
import sys
import logging

script_names = ["run_ui"]


def run_python_script(script_name, *args, **kwargs):
    logger = logging.getLogger(__name__)
    if 'profiler' in kwargs:
        use_profiler = True
    else:
        use_profiler = False

    if script_name == 'show':
        logger.info("\nAvailable scripts\n----------------")
        for s in script_names:
            logger.info(s)
        exit(0)

    if script_name == "run_ui":
        from scripts import run_ui as executable_script
    else:
        message = "Error, script_name ({}) must be one of {}".format(script_name, script_names)
        raise ValueError(message)

    if profiler:
        logger.info("running with profiler")
        command = "script.main(*args)"
        filename = "%s.prof" % script_name
        cProfile.runctx(command, None, locals(), filename=filename)
        logger.info("To see profiler result, run:\nsnakeviz %s" % filename)
    else:
        executable_script.main(*args)


if __name__ == "__main__":
    profiler = ' -p' in ' '.join(sys.argv)
    script = sys.argv[1]
    arguments = sys.argv[2:]
    # remove the profile flag now that profiler is on
    arguments = [i for i in arguments if i != '-p']
    run_python_script(script, arguments, profiler=profiler)
