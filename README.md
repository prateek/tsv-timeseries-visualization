# Description
Small python utility to render timeseries tsv files using rickshaw.js

# Assumptions
- Data file is tab seperated
- Data file has a header row
- One of the fields is called Date, is in format like '1-Jan-13'
- Rest of the fields are plotted and are numbers

# Running instructions
1. Run the following command
```
./generate_html <tsv_file> > webpage.html
```
2. Open the generated webpage 
