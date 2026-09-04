#PATCH NOTES 
## v1.0.0 

##INITIAL RELEASE

This is the first functional release of GH-graph-Automation CLI

Added : 

python CLI architecture
argparse
config validation
UTF-8 text-file filtering
Deterministic file-ordering method
commit scheduling
user-defined commits per day
user-defined commit intervals
dry-run mode
git staging, commiting and pushing

##Known Issues
-v1.0.0 has a small scope and many issues
-source repository and working repo are currently the same dicrectory , meaning the original contents may be modified during execution, this is because i dont get paid enough to solve this.
-if execution is interrupted, the repo may be left in a partially reconstructed state.
-many uneccesary comments because the dev was running on coffee and ambition
=dry run mode simulates the execution plan but does not validate every git operation that would occur during a REAL run
-git auth , remote config and push permissions are assumed to be already configured correctly
-files that cannot be decoded as UTF-8 are skipped :)
-scheduler currently operatres using the system's local time, and doesn't provide explicit timezone config, shouldnt be a problem if you're an Indian. lol imagine not being Indian

##Architecture 

This project is devided into focused modules : 
- cli.py 
- config.py
-splitter.py
-git.py
-scheduler.py
-main.py

 
