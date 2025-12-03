*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Reset And Close Browser
Test Setup       Reset Citations And Go To Home Page

*** Test Cases ***

Create Citation With Everything Empty
    Go To Create Citation Page
    Page Should Contain  Citation fields cannot be empty
    Element Should Be Disabled  id=submit_button

Create Valid Citation
    Go To Create Citation Page
    Input Text  locator=title  text=testi_title
    Input Text  locator=author  text=testi_author
    Input Text  locator=date  text=1945
    Element Should Be Enabled  id=submit_button
    Click Button  Add citation
    Page Should Contain  testi_title

Create Citation With Title Empty
    Go To Create Citation Page
    Input Text  locator=author  text=testi_author
    Input Text  locator=date  text=2020
    Page Should Contain  Citation fields cannot be empty
    Element Should Be Disabled  id=submit_button

Create Citation With Author Empty
    Go To Create Citation Page
    Input Text  locator=title  text=testi_title
    Input Text  locator=date  text=2020
    Page Should Contain  Citation fields cannot be empty
    Element Should Be Disabled  id=submit_button

Create Citation With Date Empty
    Go To Create Citation Page
    Input Text  locator=title  text=testi_title
    Input Text  locator=author  text=testi_author
    Page Should Contain  Citation fields cannot be empty
    Element Should Be Disabled  id=submit_button

Create Citation With Invalid Date
    Go To Create Citation Page
    Input Text  locator=title  text=testi_title
    Input Text  locator=author  text=testi_author
    Input Text  locator=date  text=testi_date
    Page Should Contain  Year must be between 1 and 2025!
    Element Should Be Disabled  id=submit_button

*** Keywords ***

Reset Citations And Go To Home Page
    Reset Citations
    Go To Home Page
