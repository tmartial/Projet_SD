# Projet_SD
Github for the Software Deployment project

## Documentation : 
when adding a module in package/ :
> sphinx-apidoc -f -o source/  ../package/
Modify the index.rst file to include the new files that were created by sphinx-apidoc.
Clean the output files > make clean
Execute the Makefile > make html