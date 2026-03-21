# READ ME

Main folder - src  
Name of the package - End-of-Module-Assignment  
Internal version: ** TBC **  
Version delivered: 1.0  

### What is this repository for? ###
This repository can be used to run the bring the Graphical User Interface of a travel ticketing system. This can be scaled up to develop a fully functional GUI with JSON-based storage, allowing a travel agency to manage its client database and bookings efficiently. The requirement.txt is provided for set up instructions. Any additional features can be added by improving the fields available in the gui development repository. 
We have a test suite containing a series of Pytest test cases which aid in checking if the GUI fields are working as expected and the tests are designed to highlight the errors thereby giving the test results.
The storage is JSON based and every event or record is created, appended, amended or deleted. Improvements made iteratively to each of the functions and modules built.

## The test_model, test_repository and test_storage have Pytest that can be utilised to check diverse range of feature behaviour such as:
Model Tests:    
    Validation of required fields  
    Correct dictionary serialization  
    Reconstruction from stored data  
 
Repository Tests:  
    Record creation and ID assignment  
    Referential integrity rules  
    Update validation  
    Search functionality  
    Persistence cycle  
 
Storage Tests:  
    File existence detection  
    Data saving and loading  
    Handling of missing files  
    Correct overwrite behaviour  

### How do I get set up? ###  
Python 3.13  
Windows used.  
This program can be run in Linux environment as well.  
VS Code IDE and terminal  

### Running the scripts ###  
    End-of-Module-Assignment  
        main
            -> src
                -> record
            -> README.md
            -> requirements.txt
        development
            -> data
                -> repository
                -> storage
            -> gui
                -> airline_form
                -> airline_view
                -> client_form
                -> client_view
                -> flight_form
                -> flight_view
                -> main_window
                -> search_view
            -> record
                -> airline
                -> base_record
                -> client
                -> flight
                -> record.jsonl
            -> tests
                -> test_models
                -> test_repository
                -> test_storage
        feature/night-mode
            -> data
                -> repository
                -> storage
            -> gui
                -> airline_form
                -> airline_view
                -> client_form
                -> client_view
                -> flight_form
                -> flight_view
                -> main_window
                -> search_view
            -> record
                -> airline
                -> base_record
                -> client
                -> flight
                -> record.jsonl
1) Install Requirements  
pip install -r requirements.txt  

2) Run the main.py file from root using  
python -m src.main  
            
### Context for how the tool fits into the broader ecosystem ###   
This program can be used for educational purposes. It can be used to scale the functions to be able to input more diverse features which support the ticketing interface used by the travel agent. 
This package can serve as a good starting point for students who are willing to get better in Python coding. 
The performance tests gives us an idea of the efficiency of the GUI in updating the records, searching and validation. 
This can be used for comparing performances of other GUIs pertianing the ticketing system. 

