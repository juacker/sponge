==================================================================
Sponge - Automated console connection and command execution
==================================================================

Introduction
=============

Sponge was designed to automate remote host connections and command execution in
the following situations:

 - To connect to a remote server that you reach after jumping through multiple hosts
 - When the connection chain implies multiple protocols, such as telnet, ssh, curses menus, etc (by now, only ssh support included)

 

Configuration
=============

 - Once downloaded, copy files commands.xml and servers.xml to your $HOME/.sponge directory

 - Edit servers.xml and fill it with your server configuration and customize the commands
   with the ones you want to use in commands.xml.

Requirements
=============

Python 2.5+

Pexpect >=2.3