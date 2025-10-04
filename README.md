# AAI 520 Final Project - Group 4



## Prerequisites
1. Docker: Install Docker on your machine. 
2. Visual Studio Code: Install Visual Studio Code.
3. Remote - Containers Extension: Install the "Remote - Containers" extension for VS Code from the Extensions Marketplace.

## Quick Start Guide

1. Begin by cloning the repository that contains the development container configuration:

```
git clone <repository-url>
cd <repository-directory>
```

2. Open the Project in VS Code. `code .`
3. Rebuild and Open the Container. Use the Command Palette (Ctrl+Shift+P or Cmd+Shift+P on macOS) to select Remote-Containers: Rebuild Container. VS Code will build the Docker image based on the configuration in the .devcontainer directory and open the project inside the container. *Note: You want to rebuild and reopen from the same folder this project is cloned to, otherwise vscode will create its own devcontainer at the current folder.*
4. Once inside the development container, you can use juputer notebooks (without an exposed port).

## Additional Features

#### Eporting a Jupyter Notebook as PDF. 

*Note: Current devcontainer setup has Pandoc and other packages commented out. Would need to rebuild to use this.*
You can add a `--output` flag if you want to specify the output file name otherwise it will use the file_name of your .ipynb.
```
jupyter nbconvert --to pdf <file_name.ipynb>
```

## TODO
[] 
