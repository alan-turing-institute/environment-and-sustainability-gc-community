# How we map stakeholders

<mark>*** All material in this repository is shared as a work in progress. Some material may be missing, under review, or no longer in scope. Please  [contact the E&S Senior Research Community Manager](./CONTRIBUTING.md) if you have questions about reuse or contribution. *** </mark>

## Aim
To have a comprehensive list and map of E&S GC stakeholders covering indviduals, projects and organisations which are revant to the missions of the E&S GC. 

## Method 
A combination of desk research, targeted questions (e.g. to researchers), and exploratory discussions with current stakeholders/partners (e.g. RAM meetings) were undertaken prior to September 2023. These activties identified a first set of stakeholders for TRIC-DT (n = 92) which were used to build the data collection structure upon which this map is based. The data collection structure was further devevloped in MS excel for flexibility, then once a stabel and satisfactory structure was acheived, a new set of sharepoint lists were developed for the E&S GC. 

**The sharepoint lists can be found in the E&S GC site documents. <mark>No links are provided here until we are confident that the access is appropriately controlled</mark>**



### Data Management
The complied data will be GDPR Personal and may hold reputational risk. Yhe raw data will acconrdingly be held on Turing Sharepoint with restricted access. The team will determine what outputs of this exercise (in addition to documentatio) can be shared. 


## Results


## Analysis 
<mark> This is all draft</mark>
1. Download all sharepoint lists to csv
2. Run code [sharepoint-to-kumu.py](./sharepoint-to-kumu.py) to create kumu elements and connections

## Ongoing use



==How are we going to continue to use and develop this list? Inc feedback into TPS==

<mark>'Interactions' list should be updated after each event (e.g. knowledge share, community call) to collect the attendees and their engagement levels. Could also be updated monthly with slack roundup to see who it=s active on there</mark>.

Note there is validation on the company name new entries are not allowed to contain ",". This is because sharepoint uses "," as a delimiter and we need to replace this with "|" for kumu, so our code to move the data from sharepoint to kumu repalces "," with "|" and names containing "," get broken!

