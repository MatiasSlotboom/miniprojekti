*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Reset And Close Browser
Test Setup       Reset Citations And Go To Home Page

*** Test Cases ***

Create Citation With Title Empty
    Go To Create Citation Page
    Input Text  locator=author  text=testi_author
    Input Text  locator=date  text=2020
    Click Button  Add citation
    Page Should Contain  Citation fields cannot be empty

Create Citation With Author Empty
    Go To Create Citation Page
    Input Text  locator=title  text=testi_title
    Input Text  locator=date  text=2020
    Click Button  Add citation
    Page Should Contain  Citation fields cannot be empty

Create Citation With Date Empty
    Go To Create Citation Page
    Input Text  locator=title  text=testi_title
    Input Text  locator=author  text=testi_author
    Click Button  Add citation
    Page Should Contain  Citation fields cannot be empty

*** Keywords ***

Reset Citations And Go To Home Page
    Reset Citations
    Go To Home Page

Reset And Close Browser
    Reset Citations
    Close Browser