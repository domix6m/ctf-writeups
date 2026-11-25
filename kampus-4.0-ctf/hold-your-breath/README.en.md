# Hold Your Breath

Binary Exploitation, Medium · [Polski](README.md)

The filter label is read without a terminating zero, so after entering 32 characters the Status option also prints the `puts` address, from which I calculated the address of `system` in the provided libc. `clean_filter` releases the lock and sleeps for 5 seconds before calling `f->log_func(f->label)`, so I start cleaning on one connection and, meanwhile, on the second one I eject the filter and add a log entry, which gets the same chunk of memory with my command and the `system` address. I couldn't see the output on my connection, so I first used `sleep` to check that `system()` runs, and then redirected the output to the sockets: `python3 solve.py 'cat f*>&4;cat f*>&5;cat f*>&6'`.

Scripts: [solve.py](solve.py)
