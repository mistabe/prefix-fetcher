# SECOPS ACLUPDATES

## Introduction

To automate application of all the service URLs required for applications requiring 
ACEs configured on the Firewalls.
Transform the data types that come in into usable host or CIDR ranges then use 
configuration management tooling to apply those changes to the firewalls in the 
estate.
Alert into Slack the change is required. For maximum snazz, see if the process can pick up an approval statement and act 
automatically. Otherwise manual lever pulling for the automation with an interactive command is entirely okay.  

## Getting Started

TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:

1. Installation process
2. Software dependencies
    Python 3.9.1 or above <https://www.python.org/>
    Python Azure KeyVault <https://docs.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python?tabs=cmd>
    Netmiko <http://ktbyers.github.io/netmiko/>
    Requests <https://requests.readthedocs.io/en/master/>

3. Latest releases
4. API references

## Build and Test

TODO: Describe and show how to build your code and run the tests.

## Contribute

TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)
