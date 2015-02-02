DistributedFileSystem - CS4032 Project
=====================
##Client
Provides the functionality of the distributed file system to the end user. Includes a simple main test program that allows you to specify file names and some sample file contents to facilitate quick testing of the DFS.

##File Server
Each file server node provides filesystem functionality for the distributed file system.

##Directory Server
Acts like a namenode, keeps track of where every file is in the distribute file system. In otherwords, it tracks which file server holds a particular file.

##Locking Server
Keeps track of which files are locked in the distributed file system, and which client owns the lock.

##Caching
Simple caching on the client side that will read the file from the cache if present and valid. Will check if valid with the master server before, and invalidate if not.

##Usage
"cd src" and execute "run.sh".

"run.sh" creates:
- 1 directory server
- 2 file system nodes
- 1 locking server
- 2 clients

## TODO
Clean up code, which is messy due to time constraints.