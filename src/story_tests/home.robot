*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations And Go To Home Page

*** Test Cases ***

Click Create Citation Link
    Click Link  Create new citation
    Create Citation Page Should Be Open

*** Keywords ***

Reset Citations And Go To Home Page
    Reset Citations
    Go To Home Page