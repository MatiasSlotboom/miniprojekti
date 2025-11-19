*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Reset And Close Browser
Test Setup       Reset Citations Create Test Citation And Go To Home Page

*** Test Cases ***

Click Create Citation Link
    Click Link  Create new citation
    Create Citation Page Should Be Open

One Citation Shows Up
    Page Should Contain  dated

*** Keywords ***

Reset Citations Create Test Citation And Go To Home Page
    Reset Citations
    Create Test Citation
    Go To Home Page

Reset And Close Browser
    Reset Citations
    Close Browser