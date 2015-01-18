DistributedFileSystem - CS4032 Project
=====================
##Client
Provides the functionality of the distributed file system to the end user.

##File Server
Each file server node provides filesystem functionality for the distributed file system.

##Directory Server
Acts like a namenode, keeps track of where every file is in the distribute file system. In otherwords, it tracks which file server holds a particular file.

##Locking Server
Keeps track of which files are locked in the distributed file system, and which client owns the lock.

##Usage
"run.sh" creates:
- 1 directory server
- 2 file system nodes
- 1 locking server
- 2 clients

## TODO
- Caching