*** Settings ***
Resource  resource.robot
Library         SeleniumLibrary
Library         Collections
Suite Setup      Open And Configure Browser
Suite Teardown   Reset And Close Browser
Test Setup       Reset Citations Create Test Citation And Go To Home Page

*** Test Cases ***

Click Create Citation Button
    Click Button  Create new citation
    Create Citation Page Should Be Open

One Citation Shows Up
    Page Should Contain  Testilähde

Two Citations Show Up
    Reset Citations Create Two Test Citations And Go To Home Page
    Page Should Contain  Testilähde1

    Page Should Contain  Testilähde2

*** Keywords ***

Reset Citations Create Test Citation And Go To Home Page
    Reset Citations
    Create Test Citation
    Go To Home Page

Reset Citations Create Two Test Citations And Go To Home Page
    Reset Citations
    Create Two Test Citations
    Go To Home Page
