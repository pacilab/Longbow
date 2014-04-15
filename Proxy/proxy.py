import os
import sys
from core.syscommands import SysCommands
from core.configs import HostConfig, JobConfig
from core.appcommands import Applications
from core.jobcommands import Scheduler
from core.staging import Staging

def proxy(app_args):
    
    """The main function that forms the basis for operating the core library. This can serve as a template
    for building more advanced applications. Here most of the classes are doing auto configuration through 
    the use of factory classes, however the same things can be done by calling the respective classes for
    example (scheduler can be called using the lsf or pbs class if known or preferred)."""
    
    #-----------------------------------------------------------------------------------------------
    #I find it easier using relative paths, in this case I'm going to run both the remote and local
    #paths relative to the "~" user dir. Before I set the working dir to the user dir, I capture the
    #absolute path of the hosts.conf and job.conf.
    
    #host config file (user, host, port and scheduler)
    config_file = os.getcwd() + "/hosts.conf"
    
    #add this as a commandline arg -conf
    job_file = os.getcwd() + "/job.conf"

    #Use paths relative to user dir so set this as our cwd
    os.chdir(os.path.expanduser("~"))
    
    #-----------------------------------------------------------------------------------------------
    #Instantiate the classes.
    
    jobconf = JobConfig(job_file)
    
    #Instantiate the remote connection configuration class. This is where host connections are dealt with
    #It was convenient to support different hosts this way.
    resource = HostConfig(jobconf.resource, config_file)
    
    #Instantiate the sys commands class.
    command = SysCommands(resource.user, resource.host, resource.port)
    
    #Instantiate the jobs commands class, this return the correct class for the scheduler environment. If not specified in the host.conf
    #then testing will try to determine the scheduling environment to use.
    schedule = Scheduler.test(command, resource)
    
    #Instantiate the staging class.
    stage = Staging()
    
    #Instantiate the application commands class, this will return the correct class for the application specified on command line.
    #Some tests as to whether the application is actually in your path will happen automatically.
    application = Applications.test(jobconf.program, jobconf.executable, command)
    
    #-----------------------------------------------------------------------------------------------
    #Start processing the job setup.
    application.processjob(app_args)
    
    #TODO: do something with the path to the job file here 
    #(perhaps a local working dir so this becomes more of an application and less like a script).
    schedule.jobfile("Desktop/" + "myjob.pbs", "24", "24", "8", "e280", "1","-i 1 -j 2 -k 3 -l 4")
    
    #TODO: stage all of the job files along with the scheduling script.
    
    #TODO: submit the job to the scheduler.
    #schedule.submit(command, "test.job")
    
    #-----------------------------------------------------------------------------------------------
    #Monitor jobs.
    
    #TODO: monitoring jobs and any ongoing file staging will go here.
    
    
if __name__ == "__main__":
    
    """Main entry point for the ProxyApp as a stand-alone application. The main function proxy can be hooked directly by providing it with the correct args."""
    
    #Fetch command line arguments
    command_line_args = sys.argv 
    
    #Remove the first argument (the application path)
    command_line_args.pop(0)
    
    #Enter the main application function and pass it the dictionary containing the resource + application (args) 
    #plus the list of unparsed command line arguments (command_line_args).
    proxy(command_line_args)

