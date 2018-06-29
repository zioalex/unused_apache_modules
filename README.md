# Why this ?
I'd like to know which Apache modules are really used to remove the other ones from the config files and having a smaller apache process memory footprint.

# Requirements
* apache server-info module enabled
* curl
* python3

# How is it working ?
This script is analyzing the server-info page, showing you how and where your modules are configured or used

If the module is configured but not used it will suggest to remove it.

# How to use it ?
Dump the content of Apache server-info page to a file.
The server-info page should be dumped only after the site has been used. This imply that all the modules needed are used.

  curl http://localhost/server-info > http_modules_test.txt
  cat http_modules_test.txt| python find_unused_apache_mod.py

  1
  Module name mod_python.c
  Configuration Phase Participation: 4
  Request Phase Participation: 11
  Current Configuration: 3

  2
  Module name mod_version.c
  Configuration Phase Participation: 0
  Request Phase Participation: 0
  Current Configuration: 1

  3
  Module name mod_proxy_connect.c
  Configuration Phase Participation: 0
  Request Phase Participation: 0
  Current Configuration: 0 

  To remove safely:
   ['mod_proxy_connect.c']
  POPPED:  mod_proxy_connect.c

  To KEEP:  ['mod_python.c', 'mod_version.c', 'mod_proxy_connect.c']

You can test on a real case example with:

  cat http_modules.txt| python find_unused_apache_mod.py
