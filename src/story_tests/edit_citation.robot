*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Reset And Close Browser
Test Setup       Reset Citations Create Test Citation And Go To Home Page

*** Test Cases ***

Edit Citation Title
    Go To Edit Page
    Clear Element Text  locator=title
    Input Text  locator=title  text=Testilähde1
    Submit Changes
    Page Should Contain  Testilähde1

Edit Citation Author
    Go To Edit Page
    Clear Element Text  locator=author
    Input Text  locator=author  text=Testitekijä1
    Submit Changes
    Click Link  Testilähde
    Page Should Contain  Testitekijä1

Edit Citation Date
    Go To Edit Page
    Clear Element Text  locator=date
    Input Text  locator=date  text=1950
    Submit Changes
    Click Link  Testilähde
    Page Should Contain  1950

Edit Citation Type
    Go To Edit Page
    Select From List By Value  id=type  book
    Submit Changes
    Click Link  Testilähde
    Page Should Contain  book

*** Keywords ***

Reset Citations Create Test Citation And Go To Home Page
    Reset Citations
    Create Test Citation
    Go To Home Page

Go To Edit Page
    Click Link  Testilähde
    Scroll Element Into View    id=edit-btn
    Wait Until Element Is Visible    id=edit-btn
    Click Button    edit-btn

Submit Changes
    Scroll Element Into View    id=submit_button
    Wait Until Element Is Visible    id=submit_button
    Click Element  id=submit_button