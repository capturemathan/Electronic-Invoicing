# Electronic-Invoicing 
Scanned invoices are extracted using image processing to reduce the non-reliability and man-power in calculating payments and invoice bills. Additionally, the whole payment process is automated with less turn around time and more flexibility in the invoice templates.

<img width="1024" height="512" src="images/web.jpg">

## Deliverables (as promised) :wink:
1. Accurate Prediction
2. Reducing cost of time and space
3. Automating changes and cycles
4. Reliability of data is ensured after every updation
5. Ease of access
6. Standard Invoice Format ensured
7. Scalable to any structured and unstructured documents

### A detailed explanation of the CODE and the EXECUTION is available at [E-Invoicing](https://bit.ly/flipkartinvoicing)

## Instructions (Let's get going)

`RECOMMENDED: Running in GOOGLE COLAB provides faster results and interactivity`

#### Directory Structure (Initial SETUP for COLAB & LOCALHOST)
``` bash
/flask.py
/pdfconvert.py
/digital_processing.py
/table_extraction.py
/text_extraction.py
/templates
  /index.html
/static
  /index.css
/output
  /dataset1/
    invoice.pdf
```
#### Important Points
1. `static` & `templates` are required for FLASK operation.
2. Place the TEST INVOICE inside `output/dataset1`.
3. `.py` files in the root folder are responsible for the extraction processes.
4. At any time during the entire running of the program, intermediate O/P's are present at `output/dataset1`.
5. Every `function` present in the CODE has a clear `DOCSTRING` attached to it which can be called using `help(function-name)` (or) `function-name.__doc__`

##### Running in GOOGLE COLAB 
  You can either directly mount this [Colab drive link](https://drive.google.com/drive/folders/1USPT8qZWsm1NESfjkmQFaStyImsr2mL-?usp=sharing) in your colab, change path according to the project structure from your GDrive in the code and run flask.py or follow the below mentioned steps.
1. Ensure the above directory structure is maintained by moving all the 5 `.ipynb` modules and 2 folders `static` and `templates`.
2. Connect to the runtime environment and mount the GDrive.
3. `RUN ALL Cells` in `flask.ipynb` to fire up the WEB SERVER :tada:
4. Upload the invoice
5. Initially the `CONVERT` button is blocked and after `pre-processing` it is enabled.
6. The final O/P's are available at `output/dataset1` including pre-processing steps. (In case the process is slow please refer to this directory)
7. Finally `.zip` containing all the required information is available at `output/dt1.zip`

##### Running in LOCALHOST
1. Clone the repo and extract the `localhost` code to a seperate folder.
2. `pip install -r requirements.txt` located [here](https://github.com/sathiyajith/Electronic-Invoicing/tree/master/localhost)
3. Run `python index.py` inside the directory and you're good to go :tada:
4. Upload the invoice
5. Initially the `CONVERT` button is blocked and after `pre-processing` it is enabled.
6. The final O/P's are available at `output/dataset1` including pre-processing steps. (In case the process is slow please refer to this directory)
7. Finally `.zip` containing all the required information is available at `output/dt1.zip`

If there are any issues, I request you to [mailto](mailto:sathiyajith19@gmail.com)