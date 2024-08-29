# DART Desktop App  
  
![example workflow](https://github.com/eazXneo/DART-Desktop-App/actions/workflows/python-app.yml/badge.svg)  
  
Graphical User Interface for the Deep Approximation for Retinal Traits (DART) codebase. 

From the [DART repository](https://github.com/justinengelmann/DART_retinal_fractal_dimension): "DART (Deep Approximation of Retinal Traits) allows to compute retinal traits very quickly (200-1,000 img/s on a single machine) and in a way that is more robust to image quality issues." The user interface was developed to allow for easy setup and usage of DART by bypassing the need for installing python, pytorch and various dependencies as well as basic knowledge of using the command line to enter parameters.

## Quick start

## Implementation details 
The interface itself was developed using tkinter following Object-Oriented Programming practices. tkinter was chosen due to its relative simplicity and being easy to learn. It suited the needs of this project to create a straightforward interface with native UI elements.

Testing was conducted to compare output from running the model directly vs using the interface. Passing tests indicate the result values generated when using the interface are acceptably close or identical compared with the values obtained from running the model by itself. Retinal scans from the [GRAPE dataset](https://springernature.figshare.com/articles/dataset/GRAPE_dataset_CFPs/23575926?backTo=%2Fcollections%2FGRAPE_A_multi-modal_glaucoma_dataset_of_follow-up_visual_field_and_fundus_images_for_glaucoma_management%2F6406319&file=41358156) were used as test data.

Some screenshots of the interface screens can be seen below:
![welcome screen](.github/art/welcome.png)
![basic run using DART Desktop app](.github/art/basic_run.png)
## Ackowledgements
Special thanks to [@justinengelmann](https://github.com/justinengelmann) for advice and feedback on this project.

![basic run using DART Desktop app](.github/art/splash_screen.gif)