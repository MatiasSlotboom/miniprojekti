*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Reset And Close Browser
Test Setup       Reset Citations Create Test Citation And Go To Home Page

*** Test Cases ***

Click Citation Title
    Click Link  Testilähde
    Page Should Contain  Details
    Page Should Contain  Title: Testilähde
    Page Should Contain  Author: Testitekijä
    Page Should Contain  Year: 1900

Navigate Back To Home Screen
    Click Link  Testilähde
    Page Should Contain  Details
    Click Link  Back
    Page Should Contain  Create new citation

*** Keywords ***

Reset Citations Create Test Citation And Go To Home Page
    Reset Citations
    Create Test Citation
    Go To Home Page

Reset And Close Browser
    Reset Citations
    Close Browser