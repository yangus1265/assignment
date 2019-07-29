# README

This repo contains the following:
  - assignment_1.ipynb: Jupyter notebook containing the data exploration, ETL, and modeling process related to problem 1 of the assignment. 
  - assignment_2.ipynb: Jupyter notebook containing the pandas and SQL answers to question 2 of the assignment.
  - final_prediction.pickle: the modeling output that is used to create the predictions from problem 1.
  - run.sh: the shell script that you can run in order to get a prediction. 
  
  The process is run by the following:
 
                                  ./run.sh input.csv output.csv
   
  input.csv is the input to the model. The model was trained from the following inputs:

                                   |  Variables                |
                                   |---------------------------|
                                   |  Ticket number            |
                                   |  Issue Date               |
                                   |  Issue time               |
                                   |  Meter Id                 |
                                   |  Marked Tim               |
                                   |  RP State Plate           |
                                   |  Plate Expiry Date        |
                                   |  VIN                      |
                                   |  Make                     |
                                   |  Body Style               |
                                   |  Color                    |
                                   |  Location                 |
                                   |  Route                    |
                                   |  Agency                   |
                                   |  Violation code           |
                                   |  Violation Description    |
                                   |  Fine amount              |
                                   |  Latitude                 |
                                   |  Longitude                |
                                   
  output.csv is the output of the model. The model will output the following: 
                                   
                                   | not_top_25 |  top_25   |
                                   | probability|probability|
  
  the probability ranging from 0 to 1.
  
  TODO:
  - create flask server allow for localized API call  
