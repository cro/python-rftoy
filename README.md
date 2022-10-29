# python-rftoy
Python library for controlling RF devices via the RFToy.

[RFToy](https://opensprinkler.com/product/rftoy/) is a nifty ESP8266-based device that can manipulate 433MHz remote-control
devices.  Produced by the same person who created 
[OpenSprinkler](https://opensprinkler.com) and [OpenGarage](https://opensprinkler.com/product/opengarage/), it is an
easy way to add some automation to 433MHz controlled devices.

This library implements an interface to the RFToy's HTTP server in Python.

I wrote this as a first step to adding RFToy to my Home Assistant installation.

## RFToy API

RFToy's API does not appear to be documented.  I didn't need much functionality,
just triggering different devices on and off, and seeing what RFToy thought 
their status might be.  I reverse engineered the API by reading the Arduino
source code and watching web interface interactions in browser dev tools.

The API presents a few endpoints but I only cared about two, `cc` and `jc`.  Both
take only `GET` requests.
Performing a `GET` on `jc` returns the status of all the devices RFToy knows about.
These must have been preprogrammed in advance.

Example: (formatted for readability)

```sh
    $ curl http://rftoy/jc
    { "stations": [
        {"name": "C. R. Office Light", "status": 0, "code": "09c99809c99800fa"},
        {"name": "Office Fan Low", "status": 0, "code": "09c99509c99200fa"},
        {"name": "Office Fan Med", "status": 0, "code": "09c99909c99200fa"},
        ...
        {"name": "Station 50", "status": 0, "code": "----------------"}]}
```

RFToy supports up to 50 devices.

The `cc` endpoint is where you can turn the various devices on and off.  It takes two
query parameters, `sid` (for Station ID) and `turn`.  

Example:

```sh
    $ curl http://rftoy/cc?sid=0&turn=on
    {"response":0}
```

This would turn Station 0 on ("C. R Office Light" in the example above).  I'd pass
`turn=off` to (surprise) turn off the light.

Note the RFToy does have separate 433MHz code slots for each station for "ON" and "OFF" states.
Some 433MHz devices only toggle, so the codes for ON and OFF are the same.  It's
easy for RFToy to get out of sync when that's the case.

## Using this library

The library is very small, just one file (excluding tests and project management files).
First install the dependencies.  I recommend [Poetry](https://python-poetry.org) for
dependency management, so there is a `poetry.lock` and `pyproject.toml` file.  I also exported
the dependencies to the more common `requirements.txt`.

For Poetry, run `poetry install` from the root of the project.  For Pip, run
`pip install -r requirements.txt`

There is a `__main__` clause, so if you `chmod` the `rftoy.py` file you can play
with it by typing

```sh
./rftoy 1 on
```

This would tell RFToy to turn on station 1.  You can also reference stations by their
textual names, like

```sh
./rftoy "Office Fan Low" on
```
