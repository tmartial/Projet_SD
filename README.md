# Projet_SD

## Github for the Software Development project (INSA Lyon, 4BIM, grp6)

### Project's description

Our software is a tool that can be used to elaborate a "Portait-robot", based on the similarity between given pictures and the witness memories.

### Installation instructions 


### FAQ section

- Two audiences : developers and users 
- What does the program solves ?
- Installation instructions
- FAQ section 
- Contribute section (issue tracker link, source code link)
- TODO section : functionalities to be added


## Documentation : 
when adding a module in package/ :
sphinx-apidoc -f -o source/  ../package/
Modify the index.rst file to include the new files that were created by sphinx-apidoc.
Clean the output files > make clean
Execute the Makefile > make html
