# Projet_SD : EETO 

## Github for the Software Development project (INSA Lyon, 4BIM, grp6)

### Project's description

Our software is a tool that can be used by the police to elaborate a photofit, or identikit picture (Portait-robot), based on the similarity between given pictures and the witness memories, of a person sought for a crime.

### Installation instructions 
Follow the tutorial " TUTORIAL_EETO_install_and_use.pdf " to install the software and the proper environment to use it.
You have to refer to the section that corresponds to your work environments (Linus/Mac or Windows)
If you already have the required packages installed on your machine, you don't have to go through the virtual environment steps.

### How to use the EETO software 
You can refer to the same tutorial " **TUTORIAL_EETO_install_and_use.pdf** " as for the installation instructions, starting from page 4.

### Dependencies
Please refer to requirements.txt for more detailed instructions.
- `pip install numpy` version 1.22.3
- `pip install Pillow` version 9.1.0
- `pip install tk` version 0.1.0
- `pip install keras` version 2.8.0
- `pip install python-gettext` version 4.0
- `pip install tensorflow` version 2.8.0
- `pip install matplotlib` version 3.5.1

### FAQ section

####  - Where do the initial images come from ?

They are a subset of CelebA database (http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html).

#### - How much space do I need to install the software ?

The GitHub content represents a bit more than 100Mo, and the virtual environment that you will generate to run the app is approximately 1Go.

#### - Where can I suggest improvement ideas ?

You can contact the authors, using the addresses below, and mentionning "EETO project" in object.

### TO DO 
Next release functionalities :
- Pre-select the attributes of your portrait ! For a faster and more accurate selection, the software will ask you to choose a few characteristics, in order to show already filtered faces.
- Are you feeling lost during the identification ? Click on the Help Button to see the tutorial once again, at any time. 
- Visualize the selection face portraits with an improved resolution.
- You don't really feel comfortable with using a terminal ? Run the software easily, with no command line requirements.

### Authors:
For bug reports and feedback do not hesitate to contact the authors:

- Emma Ceci: emma.ceci AT insa-lyon.fr
- Thomas Martial: thomas.martial AT insa-lyon.fr
- Emma Molière: emma.moliere AT insa-lyon.fr
- Ombeline Trancart: ombeline.trancart AT insa-lyon.fr



