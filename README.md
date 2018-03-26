# KASPA
KASPA, a simple python assistant. 
This refactoring of an assistant for a raspberry pi I had developed some months ago. It is still a work in progess.
The goal of this project is to develop an assistant that works as simple as possible, while offering all options one could want from a personal assistant.
During development I focused on keeping the code simple and making it easy to extend the functionality

## Communicators
Communicators are a way to communicate with the core of KASPA. So far I created a telegram bot, a voice communicator and a simple cli. 
However I have only tested the cli after refactoring the project
 
## Modules
To create a new module for KASPA, simply create a new class that inherits from the abstractModule.
In this class a list of regular expressions should be defined that will trigger the module. 
Furthermore KASPA expects a module name. The action method gets called, when the called query matches a regular expression from the list.
This is where the magic of the module happens. For more details check the documentation in the code.

## Dependencies
This section will be added, once a release version gets pushed.
