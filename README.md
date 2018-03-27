# K.A.S.P.A.
K.A.S.P.A., a simple python assistant.
This is a refactoring of an assistant for a raspberry pi that
I had developed some months ago. It is still a work in progess and
the code of some modules might still be a bit messy.
The goal of this project is to develop an assistant that works as
simple as possible, while offering all options one could want from a
personal assistant. During development I focused on keeping the code
simple and making it easy to extend the functionality.

## Communicators
Communicators are a way to communicate with the core_modules of KASPA.
So far I created a telegram bot, a voice communicator and a simple cli.
However I have only tested the cli after refactoring the project
 
## Modules
Modules are the heart of KASPA, as they implement the actual functionality.
Every module has an action method, that gets called when the
query matches a regular expression from a defined list.
For more details about the modules check the documentation in the code.

## Dependencies
This section will be added, once a release version gets pushed.
