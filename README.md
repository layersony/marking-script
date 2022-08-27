# Lab Marking Script

## To Install and Run Script

Clone the repository
```bash
  git clone git@github.com:layersony/marking-script.git
```
Create Virtual Environment
```bash
  python3 -m venv env_moringa
  source env_moringa/bin/activate
  pip install -r requirements.txt
```

## Marking Submissions
- Navigate to grades section in LMS 
- Click on the 3 dots on the lab of your choice
- Click on Download Submissions then download
- Extract the submissions.zip file to the marking-script folder (that you had previously cloned)
- Run the following command
```bash
  python3 marking.py
```
- The Speed for marking will be depending on the labs test and your internet

### Results

- The marks will be inside `markedCsv` under the name you gave when running the application

## Known Bugs
- Be aware of unclosed while loops or for loops